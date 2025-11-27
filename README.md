# 🎓 Academia.AI — Multi-Agent System for Automated Research Synthesis

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LangGraph](https://img.shields.io/badge/Framework-LangGraph-green)
![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen)
![Tests](https://img.shields.io/badge/Tests-Passing-success)

**Academia.AI** is a resilient, multi-agent RAG-powered system designed to ingest, analyze, and synthesize academic research papers. Built as the deliverable for **Agentic AI Developer Certification — Module 3**, this system demonstrates the transition from prototype to production-grade AI tooling.

---

## 🚀 Key Capabilities

Academia.AI enhances standard RAG pipelines with engineering-grade reliability:

- 🔁 **Self-Healing Agents:** Automatic retry logic with exponential backoff for LLM timeouts.
- 🛡️ **API Reliability Checks:** A pre-processing `HealthCheck` agent validates connectivity before workflow execution.
- 📄 **Structured Validation:** Final report must comply with a strict Pydantic JSON schema.
- 🧪 **Unit-Tested Components:** Tested ingestion workflow and keyword extraction ensure stability.

---

## 🛠 Architecture Overview

Academia.AI operates through a structured **LangGraph** workflow coordinated across three agents:

### 1. Agent: Document Ingestor
- Loads PDF/Text files.
- Splits content into semantic chunks.
- Builds an FAISS vector DB for efficient retrieval.

### 2. Agent: Thesis Extractor
- Uses NLP and keyword frequency scoring to extract hypotheses and contributions.
- Identifies core research boundaries and terminology.

### 3. Agent: Insight Synthesizer
- Retrieves relevant context from FAISS.
- Generates the final research synthesis using a retry-enabled LLM call.
- Ensures grounded output aligned with academic structure.

---

## 💻 Installation & Setup

### Prerequisites
- Python 3.10+
- OpenRouter API key

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/maddiravi/academia-ai-production.git
cd academia-ai-production
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure Environment Variables

```bash
cp .env_example .env
```

Edit `.env` with your API key:

```env
OPENROUTER_API_KEY=sk-or-v1-xxxx
OPENROUTER_API_BASE=https://openrouter.ai/api/v1
```

---

## 🏃 Running the Application

Launch the Streamlit interface:

```bash
streamlit run app.py
```

### Usage Steps

1. Upload a research paper (PDF or TXT)
2. Click **Start Analysis**
3. Watch agent logs update in real-time
4. Review generated executive summary and keyword insights

---

## 🧪 Testing & Quality Assurance

Run the automated unittest suite:

```bash
python -m unittest tests.test_academia
```

### Test Coverage Includes:

- ✔ `DocumentIngestor` workflow validation  
- ✔ Keyword extraction accuracy  
- ✔ Fault tolerance and retry path behavior  

---

## 📂 Project Structure

```
academia-ai-production/
├── agents/
│   ├── document_ingestor.py
│   ├── thesis_extractor.py
│   └── insight_synthesizer.py
├── tools/
│   ├── health_check.py
│   └── file_processor.py
├── tests/
│   └── test_academia.py
├── app.py
├── requirements.txt
└── README.md
```

---

## 🛡 License

Distributed under the **MIT License**.  
This project is open-source and free for academic and development use.

---

## 🔖 Recommended Tags

```
#AI #MultiAgentSystems #RAG #LangGraph #ResearchAutomation #Python #LLM #FAISS #Streamlit #OpenSource #AgenticAI #AIDevelopment #AcademicTools #ML #DeepLearning #KnowledgeExtraction
```
