# Design Documentation & Evaluation Report - RAG Policy Assistant

---

## Part 1: Design Documentation & Architecture Justification

### 1. Policy Corpus & Statutory Alignment
- **Corpus Structure:** 10 markdown policy files covering workplace policies (Acceptable Use, Leave, Remote Work, Dress Code, etc.).
- **Justification:** Authored with concrete South African statutory frameworks (BCEA, EEA, POPIA) to ensure realistic, legally sound organizational responses without relying on private or paid data.

### 2. Ingestion & Chunking Strategy
- **Chunking Method:** Markdown heading-based and token-window chunking with overlap.
- **Justification:** Preserves logical paragraphs and section headings, preventing the splitting of critical policy clauses across boundaries and ensuring high contextual retrieval relevance.

### 3. Embedding Model & Vector Store
- **Embedding Model:** `all-MiniLM-L6-v2` (via HuggingFace / sentence-transformers).
- **Vector Database:** Local ChromaDB (`.chroma`) storing 120 embedded chunks.
- **Justification:** MiniLM provides a lightweight, zero-cost, high-performance semantic embedding space suitable for local execution, while ChromaDB offers an efficient, zero-config local vector store.

### 4. Retrieval & Generation (RAG) & Guardrails
- **Top-$k$ Retrieval:** Retrieves the top $k$ most relevant policy chunks based on semantic similarity.
- **Prompt Strategy:** Injects retrieved chunks and explicit source citations into the context window of Groq's `llama-3.1-8b-instant`.
- **Guardrails:** Enforces strict out-of-scope refusal (*"I can only answer about our policies"*), source citation requirements, and controlled output lengths.

---

## Part 2: Evaluation Report

### 1. Overview
- **Evaluation Benchmark:** 20 Test Queries (15 In-Scope Policy Questions, 5 Out-of-Scope Prompts)
- **Inference LLM:** Groq (`llama-3.1-8b-instant`)

### 2. Performance & Quality Metrics

| Metric | Criterion | Recorded Score | Status |
| :--- | :--- | :--- | :--- |
| **Total Test Queries** | 20 Queries | 20 Queries | Complete |
| **Citation Accuracy** | Target $\ge 85\%$ | **100.0%** | **PASS** |
| **Guardrail Compliance** | Target $100\%$ Refusal | **100.0%** | **PASS** |
| **Groundedness** | Target $\ge 90\%$ | **100.0%** | **PASS** |
| **Latency (p50)** | Measured Response Time | **7.189s** | **REPORTED** |
| **Latency (p95)** | Measured Response Time | **24.885s** | **REPORTED** |

### 3. Key Findings
1. **Guardrail Protection:** Successfully filtered out-of-scope queries (general trivia, recipes) with strict policy refusals.
2. **Source Attribution:** 100% of generated answers correctly cited their respective source markdown files.
