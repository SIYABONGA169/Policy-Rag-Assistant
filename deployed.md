# Deployment Documentation

## Application Architecture

The RAG Policy Assistant is configured for WSGI deployment via Gunicorn, with the following deployment configuration:

### Local Development
- **Framework:** Flask
- **Endpoint:** http://127.0.0.1:5000
- **Execution:** Direct Flask development server for local testing and evaluation

### Production Deployment
- **WSGI Server:** Gunicorn (recommended for production)
- **Platform:** Render (placeholder configuration)
- **Status:** Pending live release
- **Production URL:** [To be updated upon live release]

---

## Deployment Notes

- **Vector Database:** ChromaDB with local persistence (`.chroma` directory)
- **Embedding Model:** all-MiniLM-L6-v2 (local execution via sentence-transformers)
- **Inference Provider:** Groq API (llama-3.1-8b-instant)
- **Environment Variables:** Configured via `.env` file (API keys, model settings)
- **Static Assets:** Web templates stored in `templates/` directory
