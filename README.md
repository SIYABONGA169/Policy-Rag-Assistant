# RAG-Based Company Policy Assistant

A web application that allows employees to query company policies and procedures using natural language. The system ingests policy documents, indexes them in a local vector database, and provides accurate answers with source citations.

## What This Project Does

This application:
- Ingests company policy documents (Markdown files) and processes them into searchable chunks
- Stores document chunks in a local vector database (ChromaDB) with embeddings
- Provides a web chat interface where employees can ask questions about company policies
- Returns answers with source document citations and text snippets for verification
- Enforces guardrails to only answer policy-related questions
- Includes an automated evaluation suite to measure system performance

## Project Prerequisites

Before you begin, ensure you have:
- **Python 3.8 or higher** installed on your Windows machine
- **Git** (optional, for version control)
- A **Groq API key** for the LLM inference engine (free at https://groq.com/)

## Setting Up the Python Virtual Environment

### 1. Create the Virtual Environment

Open PowerShell or Command Prompt in the project directory and run:

```powershell
python -m venv venv
```

This creates a virtual environment named `venv` in your project folder.

### 2. Activate the Virtual Environment (Windows)

**PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Command Prompt (cmd):**
```cmd
venv\Scripts\activate.bat
```

**Note:** If you see a PowerShell execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

After activation, your prompt should show `(venv)` at the beginning.

## Installing Required Dependencies

With the virtual environment activated, install the dependencies:

```powershell
pip install -r requirements.txt
```

This will install:
- `chromadb` - Vector database for storing document embeddings
- `sentence-transformers` - Local embedding model for generating vectors
- `python-dotenv` - Environment variable management
- `pytest` - Testing framework
- `groq` - Groq API client for LLM inference
- `flask` - Web framework for the application

## Verifying Dependencies

To verify that all dependencies are installed correctly:

```powershell
pip list
```

You should see all the packages listed in `requirements.txt` with their versions.

## Policy Documents Location

Place your company policy Markdown files (`.md`) in the following directory:

```
Company policies and procedures/
```

The system automatically discovers all `.md` files in this directory. Example filenames:
- `01_Acceptable_Use_Policy.md`
- `02_Password_and_MFA_Policy.md`
- `03_Remote_Access_VPN_Policy.md`
- And any other policy documents

**Important:** Only place policy documents in this directory. The system ingests all `.md` files found here.

## Running the Ingestion Pipeline

Before using the application, you must ingest the policy documents into the vector database.

### 1. Set Up Your Groq API Key

Create a `.env` file in the project root directory (or copy from `.env.example`):

```powershell
copy .env.example .env
```

Edit the `.env` file and add your Groq API key:

```
GROQ_API_KEY=your_actual_api_key_here
```

### 2. Run the Ingestion Script

With the virtual environment activated, run:

```powershell
python ingest.py
```

### What Successful Ingestion Produces

When ingestion completes successfully, you will see:
- A list of discovered policy documents (should be 10 files)
- Progress messages as each document is processed
- Section extraction information
- Chunk creation progress
- A summary showing:
  - Number of documents processed
  - Total chunks created
  - Total chunks in ChromaDB
  - ChromaDB persistence directory location
  - Embedding model used
  - Chunk size and overlap settings

Example output:
```
============================================================
Ingestion Complete!
============================================================
Documents processed: 10
Total chunks created: 245
Total chunks in ChromaDB: 245
ChromaDB persistence directory: .chroma
Embedding model: all-MiniLM-L6-v2
Chunk size: 500 characters
Chunk overlap: 50 characters
============================================================
```

### ChromaDB Storage Location

The ChromaDB data is persisted in the `.chroma/` directory in your project root. This directory is created automatically during the first ingestion run.

**Note:** The ingestion script clears existing data before each run to prevent duplicate chunks. It is safe to run `python ingest.py` multiple times during development.

## Starting the Web Server

After successful ingestion, start the web application:

```powershell
python main.py
```

The server will start on `http://0.0.0.0:5000` (accessible via `http://localhost:5000`).

You should see:
```
 * Running on http://0.0.0.0:5000
```

Open your web browser and navigate to `http://localhost:5000` to access the chat interface.

## Running Evaluation and Tests

The project includes an automated evaluation script that tests the system against a benchmark of policy questions.

### Run the Evaluation Suite

With the virtual environment activated and the web server stopped, run:

```powershell
python evaluate.py
```

The evaluation will:
- Test 20 benchmark questions (15 in-scope, 5 out-of-scope)
- Measure citation accuracy
- Verify guardrail compliance
- Record latency metrics (p50 and p95)
- Generate a report in `evaluation_results.csv`

### Expected Output

The evaluation script prints:
- Individual question results with latency
- Summary metrics including:
  - Citation accuracy percentage
  - Guardrail compliance percentage
  - p50 and p95 latency
  - Success/failure counts

Results are saved to `evaluation_results.csv` for detailed analysis.

## Troubleshooting

### Issue: "Policies directory not found"
**Cause:** The `Company policies and procedures/` directory does not exist.
**Solution:** Ensure the directory exists in the project root and contains your `.md` policy files.

### Issue: "No module named 'chromadb'" (or other import errors)
**Cause:** Dependencies not installed or virtual environment not activated.
**Solution:**
1. Ensure virtual environment is activated (look for `(venv)` in prompt)
2. Run `pip install -r requirements.txt`

### Issue: "GROQ_API_KEY not found"
**Cause:** Missing or incorrect `.env` file.
**Solution:**
1. Create `.env` file in project root
2. Add `GROQ_API_KEY=your_key_here`
3. Ensure no extra spaces around the equals sign

### Issue: Ingestion creates duplicate chunks
**Cause:** Running ingestion multiple times without clearing existing data.
**Solution:** The current implementation automatically clears existing data before each run. If you see duplicates, delete the `.chroma/` directory and run ingestion again:
```powershell
Remove-Item -Recurse -Force .chroma
python ingest.py
```

### Issue: Web server won't start (port 5000 already in use)
**Cause:** Another application is using port 5000.
**Solution:** Either stop the other application or modify the port in `main.py` (line 73) to a different port.

### Issue: Evaluation fails with connection errors
**Cause:** Web server not running or Groq API key invalid.
**Solution:**
1. Ensure the web server is running (`python main.py`)
2. Verify your Groq API key in `.env` is valid
3. Check your internet connection

### Issue: PowerShell execution policy error when activating venv
**Cause:** PowerShell restricts script execution by default.
**Solution:** Run this command once (as current user):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Project Structure

```
Policy and procedure Rag Application/
├── Company policies and procedures/  # Policy .md files
├── .chroma/                          # ChromaDB vector database (auto-created)
├── .env                              # API keys and configuration
├── .env.example                      # Example environment file
├── ingest.py                         # Document ingestion script
├── main.py                           # Flask web server
├── rag.py                            # RAG pipeline logic
├── evaluate.py                       # Evaluation script
├── requirements.txt                  # Python dependencies
├── templates/                        # HTML templates
│   └── index.html                    # Web chat interface
└── README.md                         # This file
```

## Technical Details

- **Embedding Model:** `all-MiniLM-L6-v2` (local, sentence-transformers)
- **Chunk Size:** 500 characters
- **Chunk Overlap:** 50 characters
- **Vector Database:** ChromaDB (persistent, embedded)
- **LLM:** Groq API (LPU inference)
- **Web Framework:** Flask
- **Collection Name:** `policy_documents`

## Security Notes

- Never commit your `.env` file or API keys to version control
- The `.env` file is already in `.gitignore`
- Use environment variables for all sensitive configuration
