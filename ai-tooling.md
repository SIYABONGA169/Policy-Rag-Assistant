# AI Tooling Documentation

## AI Tools Used

### Gemini (Google AI)
- **Purpose:** Research, architecture planning, requirement verification, and prompt strategy design
- **Usage:** Leveraged for rapid exploration of RAG patterns, evaluation methodologies, and ensuring strict alignment with assignment rubric guidelines

### Windsurf IDE with Cascade Agent
- **Purpose:** Primary AI-powered IDE for code development, workspace auditing, refactoring, script execution, and repository cleanup
- **Usage:** 
  - Developed core application files (main.py, ingest.py, evaluate.py, rag.py)
  - Performed automated workspace audits and duplicate file cleanup
  - Verified document chunking and ingestion pipeline
  - Executed test scripts and evaluation benchmarks

### Groq API (llama-3.1-8b-instant)
- **Purpose:** Primary inference provider for RAG query processing
- **Usage:** Fast, low-latency LLM inference for generating policy answers with strict guardrail enforcement and source citation requirements

### ChromaDB & sentence-transformers (all-MiniLM-L6-v2)
- **Purpose:** Document vector embeddings and similarity retrieval
- **Usage:** 
  - Local, zero-cost embedding generation using all-MiniLM-L6-v2
  - Efficient vector storage and retrieval via ChromaDB
  - Semantic search across 120 policy chunks with metadata tracking

---

## What Worked Well

- **Fast Research and Evaluation:** Gemini enabled rapid exploration of RAG patterns and evaluation methodologies, ensuring strict alignment with rubric guidelines
- **Rapid Code Development:** Windsurf IDE accelerated development of core application files with automated refactoring and error detection
- **Automated Workspace Cleanup:** Cascade Agent efficiently identified and removed duplicate policy files, maintaining a clean repository structure
- **High Citation Accuracy:** Achieved 100% citation accuracy in mapping generated answers back to correct source markdown files
- **Strict Guardrail Enforcement:** Successfully tuned guardrails to reject out-of-scope prompts with standard refusal messages
- **Local Execution:** Zero-cost local embedding and vector storage eliminated dependency on external vector services

---

## Challenges / What Didn't

- **Tool Execution Nuances:** File path syntax and tool execution in Windsurf required clear, structured prompt directions to avoid errors
- **Environment Variable Management:** Aligning local environment variables (.env) with cloud deployment configurations required careful coordination
- **Dependency Alignment:** Ensuring consistent Python dependencies between local development environment and potential cloud deployment platforms
- **Latency Optimization:** Initial latency measurements (p50: 7.189s, p95: 24.885s) exceeded targets, requiring further optimization for production readiness
