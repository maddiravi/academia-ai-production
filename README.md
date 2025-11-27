# 🎓 Academia.AI: Production-Ready Research Synthesis

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LangChain](https://img.shields.io/badge/Framework-LangGraph-green)
![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen)
![Tests](https://img.shields.io/badge/Tests-Passing-success)

**Academia.AI** is a resilient, multi-agent AI system designed to ingest, analyze, and synthesize complex academic research papers. Built as the capstone for the **Agentic AI Developer Certification (Module 3)**, this project demonstrates a transition from prototype to production-grade software.

---

## 🚀 Key Features (Module 3 Enhancements)

This system goes beyond basic RAG by implementing strict operational guardrails:

* **Self-Healing Agents:** The `InsightSynthesizer` utilizes a custom retry loop with exponential backoff to handle LLM timeouts gracefully.
* **API Guardrails:** A pre-flight `HealthCheck` mechanism validates API connectivity and key permissions before processing begins, preventing wasted tokens.
* **Structured Output:** Uses Pydantic validation to ensure the final report follows a strict JSON schema (Novelty, Summary, Discussion Points).
* **Comprehensive Testing:** Includes a `unittest` suite covering keyword extraction logic and document ingestion flows.

---

## 🛠️ Architecture

The system orchestrates three specialized agents using a **LangGraph** workflow:

1.  **Agent 1: Document Ingestor**
    * Loads PDF/Text files.
    * Splits content into semantic chunks.
    * Builds a local FAISS vector store for retrieval.

2.  **Agent 2: Thesis Extractor**
    * Analyzes the raw text to extract core arguments and keywords.
    * Uses NLP techniques to identify the paper's primary contribution.

3.  **Agent 3: Insight Synthesizer**
    * Combines the "Thesis" (from Agent 2) with "Context" (retrieved from Agent 1).
    * Generates a final executive summary using a retry-enabled LLM call.

---

## 💻 Installation & Setup

### Prerequisites
* Python 3.10 or higher
* An API Key from OpenRouter (or OpenAI)

### 1. Clone the Repository
```bash
git clone [https://github.com/maddiravi/academia-ai-production.git](https://github.com/maddiravi/academia-ai-production.git)
cd academia-ai-production
