import os
import logging
import time
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from pydantic import ValidationError # Ensure this is imported for clean error handling

logger = logging.getLogger("InsightSynthesizer")

# --- Pydantic Schema ---
class InsightSummary(BaseModel):
    novel_title: str = Field(description="A concise, attention-grabbing title for the paper summary.")
    executive_summary: str = Field(description="A one-paragraph summary detailing the motivation, method, and conclusion.")
    discussion_points: list[str] = Field(description="3-5 critical discussion points or future research directions.")

class InsightSynthesizerAgent:
    MAX_RETRIES = 3 # Operational Resilience Parameter

    def __init__(self, retriever):
        self.llm = ChatOpenAI(
            model="openai/gpt-3.5-turbo",  
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),
            openai_api_base="https://openrouter.ai/api/v1",
            temperature=0.3,
            request_timeout=30.0 # Explicit Timeout Management
        )
        self.retriever = retriever

    def generate_final_summary(self, original_content: str, thesis_data: dict):
        retrieved_docs = self.retriever.invoke("synthesize the main argument, methodology, and key results")
        retrieved_context = "\n---\n".join([doc.page_content for doc in retrieved_docs])
        
        prompt_template = PromptTemplate(
            template="""You are an expert academic synthesizer. Your task is to analyze the research paper content and generate a structured summary.
            
            RETRIEVED CONTEXT: {context}
            EXTRACTED THESIS DATA: {thesis_data}
            
            Generate the required structured summary.
            {format_instructions}
            """,
            input_variables=["context", "thesis_data"],
            partial_variables={"format_instructions": JsonOutputParser(pydantic_object=InsightSummary).get_format_instructions()},
        )

        full_prompt = prompt_template.invoke({"context": retrieved_context, "thesis_data": thesis_data})
        parser = JsonOutputParser(pydantic_object=InsightSummary)

        # --- RESILIENCE LOOP ---
        for attempt in range(self.MAX_RETRIES):
            try:
                logger.info(f"Attempt {attempt + 1}/{self.MAX_RETRIES} to invoke LLM.")
                response = self.llm.invoke(full_prompt.text)
                parsed_data = parser.parse(response.content)
                logger.info("LLM synthesis successful.")
                return parsed_data
            
            except Exception as e:
                # Catch ValidationErrors or Network errors
                logger.warning(f"LLM API Failure (Attempt {attempt + 1}): {e}")
                
                if attempt + 1 == self.MAX_RETRIES:
                    logger.error("Max retries reached. Synthesis failed permanently.")
                    raise RuntimeError("LLM generation failed after maximum retries.") from e
                
                time.sleep((2 ** attempt) + 1) # Exponential backoff

        return {"error": "Unknown synthesis failure."}