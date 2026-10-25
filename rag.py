"""
RAG Pipeline for Company Policy Assistant

This script implements FR-2, FR-3, and FR-4:
- FR-2: Retrieval & Query Processing Pipeline
- FR-3: Context Guardrails & Refusals
- FR-4: Citation & Source Snippet Attribution
"""

import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from groq import Groq


# Load environment variables first
load_dotenv()

# Configuration (must match ingest.py)
CHROMA_PERSIST_DIR = ".chroma"
COLLECTION_NAME = "policy_documents"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 4  # Number of relevant chunks to retrieve
BROAD_QUERY_TOP_K = 15  # Number of chunks to retrieve for broad/overview queries
SIMILARITY_THRESHOLD = 0.0  # Disabled - all queries pass through
GROQ_MODEL = os.getenv('GROQ_MODEL', 'openai/gpt-oss-20b')  # Groq model for inference


class RAGPipeline:
    """RAG pipeline for answering policy questions with citations."""
    
    def __init__(self):
        """Initialize the RAG pipeline with ChromaDB, embedding model, and Groq client."""
        print(f"Loading embedding model: {EMBEDDING_MODEL}")
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        
        print(f"Connecting to ChromaDB: {CHROMA_PERSIST_DIR}")
        self.chroma_client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
        self.collection = self.chroma_client.get_collection(name=COLLECTION_NAME)
        
        # Initialize Groq client
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError(
                "GROQ_API_KEY not found in environment variables. "
                "Please set it in your .env file or environment."
            )
        self.groq_client = Groq(api_key=groq_api_key)
        print(f"Initialized Groq client with model: {GROQ_MODEL}")
    
    def _is_broad_query(self, query: str) -> bool:
        """
        Detect if the query is a broad/overview request about policies.
        
        Args:
            query: User question
            
        Returns:
            True if the query is asking for a list, summary, or overview of policies
        """
        query_lower = query.lower()
        broad_patterns = [
            'list all', 'what policies', 'what procedures', 'summarize',
            'overview', 'all policies', 'all procedures', 'company rules',
            'available policies', 'what are the policies', 'policy list'
        ]
        return any(pattern in query_lower for pattern in broad_patterns)
    
    def _retrieve_context(self, query: str, is_broad: bool = False) -> tuple[List[Dict[str, Any]], float]:
        """
        Retrieve relevant policy chunks for the query.
        
        Args:
            query: User question
            
        Returns:
            Tuple of (retrieved_chunks, max_similarity_score)
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Search ChromaDB - use more results for broad queries
        n_results = BROAD_QUERY_TOP_K if is_broad else TOP_K
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        # Process results
        chunks = []
        max_similarity = 0.0
        
        if results['documents'] and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                # Convert distance to similarity (ChromaDB uses cosine distance)
                distance = results['distances'][0][i]
                similarity = 1.0 - distance
                max_similarity = max(max_similarity, similarity)
                
                chunk = {
                    'text': results['documents'][0][i],
                    'filename': results['metadatas'][0][i]['filename'],
                    'section': results['metadatas'][0][i]['section'],
                    'similarity': similarity
                }
                chunks.append(chunk)
        
        return chunks, max_similarity
    
    def _build_prompt(self, query: str, context_chunks: List[Dict[str, Any]], is_broad: bool = False) -> str:
        """
        Build the LLM prompt with retrieved context.
        
        Args:
            query: User question
            context_chunks: Retrieved policy chunks
            
        Returns:
            Formatted prompt for the LLM
        """
        context_text = "\n\n---\n\n".join([
            f"Document: {chunk['filename']}\nSection: {chunk['section']}\nContent: {chunk['text']}"
            for chunk in context_chunks
        ])
        
        if is_broad:
            prompt = f"""You are an HR and IT policy assistant for Apex Global Technologies. 
You must ONLY answer questions using the provided context extracted from company policy documents.
If a user asks a question that is outside the scope of company policies, IT guidelines, or labor regulations (such as general knowledge, recipes, geography, sports, etc.), you MUST strictly refuse by replying: 
"I can only answer questions related to company policies."
Do not attempt to answer out-of-scope questions. Always cite the specific policy document used for valid answers.

The user is asking for an overview or list of company policies. Based on the provided policy context, provide a comprehensive summary or list of the available policies and procedures.

Context:
{context_text}

Question: {query}

Instructions:
1. Provide a summary or list of the key company policies and procedures based on the context.
2. Group related policies together (e.g., security policies, HR policies, etc.)
3. For each policy mentioned, provide a brief description of what it covers.
4. Be comprehensive but concise.
5. Write in a natural, conversational tone as if you're talking to a colleague.
6. You MUST mention the document name (e.g., "01_Acceptable_Use_Policy.md") when referring to information from that document.
7. Do NOT use markdown symbols like asterisks (**), hashes (#), or horizontal rules (---). Use plain text only.
8. NEVER use double asterisks (**) around titles or headers. Use plain text like "Purpose:" or "Annual Leave:" instead.
9. Format your response with clean, readable layout:
   - Use natural paragraphs for introductions, summaries, or general answers
   - Use dash bullet points (-) ONLY when listing multiple specific items, rules, or key takeaways where a list makes logical sense
   - Do NOT force every sentence to start with a dash
   - Place the title and description together smoothly on one clean line (e.g., "- Purpose: The policy sets out...")
   - Avoid double-dashing sub-lines (do not use "- Title" followed by "- Description")
   - Keep double line breaks between paragraphs and list items for readability
   - Example format:
     
     Here's a summary of the key policies.

     - Security Policy (02_Password_and_MFA_Policy.md): This covers password requirements and access controls. Passwords must be at least 12 characters and changed every 90 days.

     - HR Policy (08_Leave_and_Time_Off_Policy.md): This covers leave requests and working hours. Employees can request up to 20 days of annual leave.

Answer:"""
        else:
            prompt = f"""You are an HR and IT policy assistant for Apex Global Technologies. 
You must ONLY answer questions using the provided context extracted from company policy documents.
If a user asks a question that is outside the scope of company policies, IT guidelines, or labor regulations (such as general knowledge, recipes, geography, sports, etc.), you MUST strictly refuse by replying: 
"I can only answer questions related to company policies."
Do not attempt to answer out-of-scope questions. Always cite the specific policy document used for valid answers.

Answer the following question using ONLY the provided policy context. Do not use outside knowledge or invent information.

Context:
{context_text}

Question: {query}

Instructions:
1. Answer the question based on the provided policy context in a natural, conversational tone.
2. If the context does not contain information to answer the question, say that you don't have that information in the policies.
3. Write as if you're talking to a colleague - be friendly and approachable.
4. You MUST mention the document name (e.g., "01_Acceptable_Use_Policy.md") when providing information from that document.
5. Be accurate but conversational.
6. Do NOT use markdown symbols like asterisks (**), hashes (#), or horizontal rules (---). Use plain text only.
7. NEVER use double asterisks (**) around titles or headers. Use plain text like "Purpose:" or "Annual Leave:" instead.
8. Format your response with clean, readable layout:
   - Use natural paragraphs for introductions, summaries, or general answers
   - Use dash bullet points (-) ONLY when listing multiple specific items, rules, or key takeaways where a list makes logical sense
   - Do NOT force every sentence to start with a dash
   - Place the title and description together smoothly on one clean line (e.g., "- Purpose: The policy sets out...")
   - Avoid double-dashing sub-lines (do not use "- Title" followed by "- Description")
   - Keep double line breaks between paragraphs and list items for readability
   - Example format:
     
     According to 02_Password_and_MFA_Policy.md, the password policy requires strong passwords for all accounts.

     - Passwords must be at least 12 characters long
     - Passwords must be changed every 90 days
     - Passwords cannot be reused within the last 5 changes

Answer:"""
        
        return prompt
    
    def answer_question(self, query: str, chat_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """
        Answer a policy question with citations and source snippets.
        
        Args:
            query: User question
            chat_history: Optional list of previous conversation messages
            
        Returns:
            Dictionary with 'answer', 'citations', and 'snippets' keys
        """
        # Validate query
        if not query or not query.strip():
            return {
                'answer': 'Please enter a question about company policies and procedures.',
                'citations': [],
                'snippets': []
            }
        
        # Check if this is a broad/overview query for context retrieval
        is_broad = self._is_broad_query(query)
        
        # Retrieve relevant context
        chunks, max_similarity = self._retrieve_context(query, is_broad=is_broad)
        
        print(f"Retrieved {len(chunks)} chunks with max similarity: {max_similarity:.3f}")
        
        # Build prompt with context
        prompt = self._build_prompt(query, chunks, is_broad=is_broad)
        
        # Call Groq API
        try:
            response = self.groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,  # Lower temperature for more factual responses
                max_tokens=500
            )
            answer = response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error calling Groq API: {e}")
            return {
                'answer': f"I apologize, but I encountered an error while processing your request: {str(e)}",
                'citations': [],
                'snippets': []
            }
        
        # Extract citations and snippets from retrieved chunks
        citations = []
        snippets = []
        
        for chunk in chunks:
            citations.append({
                'filename': chunk['filename'],
                'section': chunk['section']
            })
            snippets.append(chunk['text'])
        
        return {
            'answer': answer,
            'citations': citations,
            'snippets': snippets
        }


def answer_question(query: str, chat_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
    """
    Main entry point for answering policy questions.
    
    Args:
        query: User question
        chat_history: Optional list of previous conversation messages
        
    Returns:
        Dictionary with 'answer', 'citations', and 'snippets' keys
    """
    pipeline = RAGPipeline()
    return pipeline.answer_question(query, chat_history=chat_history)


if __name__ == "__main__":
    # Simple test when run directly
    import sys
    
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "What is the acceptable use policy?"
    
    print(f"\nQuestion: {query}\n")
    result = answer_question(query)
    
    print(f"\nAnswer:\n{result['answer']}\n")
    print(f"Citations:")
    for citation in result['citations']:
        print(f"  - {citation['filename']}: {citation['section']}")
    print(f"\nSnippets:")
    for i, snippet in enumerate(result['snippets'], 1):
        print(f"  {i}. {snippet[:100]}...")
