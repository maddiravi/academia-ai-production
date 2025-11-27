import streamlit as st
import os
import time
import logging
import re      
from dotenv import load_dotenv
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# Import Agents and Tools
from agents.document_ingestor import DocumentIngestorAgent 
from agents.thesis_extractor import ThesisExtractorAgent 
from agents.insight_synthesizer import InsightSynthesizerAgent 
from tools.file_processor import save_uploaded_file
from tools.health_check import check_openrouter_api_health # NEW IMPORT

# --- LOGGING CONFIGURATION ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

# --- STATE DEFINITION ---
class AgentState(TypedDict):
    file_path: str
    original_content: str
    chunks: list
    retriever: object
    thesis_data: dict
    summary_output: dict

# --- AGENT NODES (Unchanged) ---
def run_document_ingestor(state: AgentState):
    logger.info("Starting Document Ingestion.")
    st.info("Agent 1: Ingesting document and creating RAG index...")
    
    try:
        agent = DocumentIngestorAgent(state['file_path'])
        chunks, full_content = agent.process_document()
        retriever = agent.create_retriever(chunks)
        logger.info("Ingestion successful.")
        return {"original_content": full_content, "chunks": chunks, "retriever": retriever}
    except Exception as e:
        logger.error(f"Ingestion Failed: {e}")
        return {"error": str(e)}

def run_thesis_extractor(state: AgentState):
    logger.info("Starting Thesis Extraction.")
    st.info("Agent 2: Extracting Thesis and Key Findings...")
    
    if state.get('error'): return state
    
    try:
        agent = ThesisExtractorAgent()
        thesis_data = agent.extract_thesis_data(state['original_content'])
        logger.info("Extraction successful.")
        return {"thesis_data": thesis_data}
    except Exception as e:
        logger.warning(f"Extraction failed: {e}. Gracefully continuing.")
        return {"thesis_data": {"keywords": [], "error": str(e)}}

def run_insight_synthesizer(state: AgentState):
    logger.info("Starting Final Synthesis.")
    st.info("Agent 3: Synthesizing Final Academic Summary...")
    
    if state.get('error'): return state

    agent = InsightSynthesizerAgent(state['retriever'])
    summary_output = agent.generate_final_summary(state['original_content'], state['thesis_data'])
    
    return {"summary_output": summary_output}

# --- ORCHESTRATION ---
def create_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("ingest", run_document_ingestor)
    workflow.add_node("extract", run_thesis_extractor)
    workflow.add_node("synthesize", run_insight_synthesizer)
    workflow.add_edge(START, "ingest")
    workflow.add_edge("ingest", "extract")
    workflow.add_edge("extract", "synthesize")
    workflow.add_edge("synthesize", END)
    return workflow.compile()

# --- UI MAIN (The Final Fix) ---
def main():
    st.set_page_config(page_title="Academia Analyzer (Module 3)", layout="wide")
    st.title("🎓 Academia.ai - The Production-Ready Research Synthesis Analyzer")
    st.markdown("A production-ready Multi-Agent RAG system for academic research synthesis. Features self-healing agents, API guardrails, and comprehensive testing.")
    st.markdown("---")

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        st.error("FATAL: API Key missing.")
        return

    # --- ENHANCED SIDEBAR ---
    st.sidebar.title("System Specifications")
    st.sidebar.markdown("### Technical Stack")
    st.sidebar.markdown("* **Orchestration:** LangGraph (3 Agents)")
    st.sidebar.markdown("* **LLM Provider:** OpenRouter (GPT-3.5-Turbo)")
    st.sidebar.markdown("* **RAG:** FAISS + MiniLM Embeddings")
    
    st.sidebar.markdown("### Production Features")
    st.sidebar.markdown("- ✅ **Resilience:** Retry Logic")
    st.sidebar.markdown("- ✅ **Guardrails:** Health Checks & Input Validation")
    st.sidebar.markdown("- ✅ **QA:** Logging Enabled")

    st.header("1. Upload Research Document")
    
    uploaded_file = st.file_uploader("Upload Research Paper", type=["pdf", "txt"])
    
    if st.button("🚀 Start Analysis"):
        if not uploaded_file:
            st.error("Please upload a file.")
            return

        # --- HEALTH CHECK GUARDRAIL ---
        if not check_openrouter_api_health(api_key):
             st.error("API Health Check Failed. Service unreachable.")
             return
        
        file_path = save_uploaded_file(uploaded_file)
        app = create_graph()
        
        try:
            final_state = app.invoke({"file_path": file_path})
            
            summary_output = final_state.get('summary_output', {})

            if summary_output.get('error'):
                st.error(f"Analysis failed during synthesis: {summary_output['error']}")
            else:
                st.success("Analysis Complete! Generating Final Report...")
                st.markdown("---")
                
                # --- POLISHED OUTPUT RENDERING (FIXING JSON DISPLAY) ---
                
                st.markdown("### **🌟 Core Synthesis**")
                st.markdown(f"**Novel Title:** **{summary_output.get('novel_title', 'N/A')}**")
                st.markdown("---")

                st.markdown(f"**Primary Hypothesis:** {summary_output.get('key_hypothesis', 'N/A')}")
                
                st.markdown("### **📝 Executive Summary**")
                st.markdown(summary_output.get('executive_summary', 'N/A'))
                
                st.markdown("### **💡 Discussion Points**")
                
                # Format the discussion points list cleanly
                discussion_points = summary_output.get('discussion_points', [])
                if isinstance(discussion_points, list):
                    st.markdown("*" + "\n* ".join(discussion_points))
                
        except Exception as e:
            st.error(f"Workflow failed: {e}")
            logger.critical(f"Workflow Critical Fail: {e}")
        
        # Clean up the saved file after analysis
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    main()