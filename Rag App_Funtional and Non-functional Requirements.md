# System Requirements Specification (SRS)
**Project Title:** RAG-Based Company Policy Assistant
**Status:** Definitive Architecture Scope

---

## 1. Executive Summary & Tech Stack

This document establishes the definitive functional and non-functional requirements for the RAG-Based Company Policy Assistant. The application ingests internal company policy documents, indexes them into a local vector store, and provides an interactive web interface for employees to query company procedures with precise citations and source snippets.

### System Architecture Summary
- **Web Framework:** Python web framework (REST API server handling routing and business logic)
- **User Interface:** HTML / JavaScript / CSS (Lightweight Web Chat Interface served via the web framework)
- **Vector Database:** ChromaDB (Embedded persistent vector database for policy chunk index)
- **Embeddings Model:** sentence-transformers (Local embedding model for dense vector generation)
- **LLM Inference Engine:** Groq API (Groq LPU API for context-grounded response generation)
- **Evaluation Framework:** Python Script + CSV (Automated script measuring groundedness, citation accuracy, and latency)
- **CI/CD Pipeline:** GitHub Actions (Automated workflow executing dependency installs, build checks, and Render deployment)
- **Cloud Deployment:** Render (Production web hosting platform)

---

## 2. Functional Requirements (FRs)

### FR-1: Document Ingestion & Storage
- The system must ingest and parse company policy documents in Markdown (`.md`), HTML, PDF, and TXT formats.
- The system must split documents into text chunks using fixed token/character windows with defined overlap.
- The system must generate vector embeddings using `sentence-transformers`.
- The system must store vector chunks in `ChromaDB` alongside source metadata (document ID, section title, filename).

### FR-2: Retrieval & Query Processing Pipeline
- The system must accept user questions, generate query embeddings using `sentence-transformers`, and execute Top-k semantic retrieval against `ChromaDB`.
- The system must build a structured prompt containing the retrieved context chunks.
- The system must transmit the context payload to the `Groq API` for response generation.

### FR-3: Context Guardrails & Refusals
- The system must enforce strict context grounding guardrails.
- When a user question cannot be answered using the provided policy corpus, the system must output the exact standardized refusal:
  > `"I can only answer questions related to company policies and procedures."`

### FR-4: Citation & Source Snippet Attribution
- The system must append source document titles and section identifiers to every generated policy answer.
- The system must return the exact text snippets and document IDs in the API response payload for user verification.

### FR-5: Application Endpoints & User Interface
The web application must expose three mandatory endpoints:
1. `GET /` : Serves the HTML/JS web chat interface.
2. `POST /chat` : Accepts JSON requests (`{"question": "..."}`) and returns JSON containing model answer, citations, and source snippets.
3. `GET /health` : Returns JSON status (`{"status": "healthy"}`) for system health monitoring on Render.

### FR-6: Quantitative System Evaluation Suite
- The project must include an automated Python evaluation script evaluated against a benchmark of 15–30 policy questions.
- The script must generate a report measuring:
  - **Groundedness:** % factually supported content
  - **Citation Accuracy:** % correct citations
  - **Request Latency:** p50 and p95 percentiles in seconds

---

## 3. Non-Functional Requirements (NFRs)

### NFR-1: Performance & Latency SLAs
- The system must achieve a median (p50) request latency of under 2.5 seconds.
- The system must achieve a 95th percentile (p95) latency of under 5.0 seconds for standard queries using the Groq API and ChromaDB vector search.

### NFR-2: Reproducibility & Determinism
- All Python dependencies must be locked in `requirements.txt`.
- Fixed random seeds must be configured across chunking and evaluation sampling modules to ensure deterministic test execution and reproducible metrics.

### NFR-3: Production Hosting Constraints (Render)
- The application must be deployed and hosted on Render.
- The application startup sequence, memory consumption, and static assets must comply with Render's web service execution environment.

### NFR-4: Automated CI/CD Pipeline (GitHub Actions)
- The project must use a GitHub Actions workflow triggered on every code push or Pull Request to the `main` branch.
- The workflow must install dependencies, run build checks, execute smoke tests, and trigger deployment to Render via Deploy Hook.

### NFR-5: Security & API Key Management
- The `GROQ_API_KEY` must not be hardcoded or committed to version control.
- Credentials must be injected dynamically via environment variables (`.env` files locally and Render Environment Variables in production).