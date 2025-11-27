import os
import re
import json
import logging
from collections import Counter
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
import nltk
from nltk.corpus import stopwords

# --- Logging ---
logger = logging.getLogger("ThesisExtractor")

# --- NLTK Setup ---
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

# --- Pydantic Schema ---
class ExtractedThesis(BaseModel):
    primary_hypothesis: str = Field(description="The main hypothesis or claim of the paper.")
    methodology_keywords: list[str] = Field(description="5-7 technical keywords representing the methods.")
    key_findings: str = Field(description="The single most important conclusion.")

class ThesisExtractorAgent:
    """Agent 2: Extracts core academic data using both NLP and LLM."""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        # LLM for deep extraction
        self.llm = ChatOpenAI(
            model="openai/gpt-3.5-turbo",  
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),
            openai_api_base="https://openrouter.ai/api/v1",
            temperature=0.1
        )

    # --- 1. NLP Method (Required for Unit Test) ---
    def _clean_text(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', '', text)
        return text

    def extract_keywords(self, content: str, top_n: int = 15) -> list:
        """Extracts frequent technical keywords (Used by Unit Tests)."""
        cleaned_text = self._clean_text(content)
        words = cleaned_text.split()
        keywords = [word for word in words if word not in self.stop_words and len(word) > 2]
        
        word_counts = Counter(keywords)
        return [word for word, count in word_counts.most_common(top_n)]

    # --- 2. LLM Method (Required for Main App) ---
    def extract_thesis_data(self, content: str):
        """Uses LLM to parse structured data, with NLP keywords as backup."""
        
        # Run NLP extraction first (fast & cheap)
        nlp_keywords = self.extract_keywords(content)
        
        # Prepare content for LLM
        MAX_TOKENS = 4000
        truncated_content = content[:MAX_TOKENS]

        prompt_template = PromptTemplate(
            template="""You are an expert thesis extractor. Analyze the text and extract the hypothesis, findings, and methodology.
            
            TEXT SAMPLE: {content}
            
            {format_instructions}
            """,
            input_variables=["content"],
            partial_variables={"format_instructions": JsonOutputParser(pydantic_object=ExtractedThesis).get_format_instructions()},
        )

        parser = JsonOutputParser(pydantic_object=ExtractedThesis)
        full_prompt = prompt_template.invoke({"content": truncated_content})

        try:
            logger.info("Invoking LLM for thesis extraction...")
            response = self.llm.invoke(full_prompt.text)
            parsed_data = parser.parse(response.content)
            
            # Merge NLP keywords if LLM missed them or just to enrich data
            if not parsed_data.get('methodology_keywords'):
                parsed_data['methodology_keywords'] = nlp_keywords[:5]
                
            return parsed_data
        
        except Exception as e:
            logger.error(f"LLM Extraction Failed: {e}")
            # Fallback to basic NLP data if LLM fails
            return {
                "primary_hypothesis": "Extraction Failed",
                "methodology_keywords": nlp_keywords[:7],
                "key_findings": "N/A"
            }