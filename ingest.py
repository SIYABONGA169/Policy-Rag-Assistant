"""
Document Ingestion Script for RAG-Based Company Policy Assistant

This script implements FR-1: Document Ingestion & Storage
- Parses company policy documents from Markdown files
- Chunks text using fixed character windows with overlap
- Generates embeddings using sentence-transformers
- Stores chunks in persistent ChromaDB with metadata
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Optional

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer


# Configuration
POLICIES_DIR = "Company policies and procedures"
CHROMA_PERSIST_DIR = ".chroma"
CHUNK_SIZE = 500  # characters
CHUNK_OVERLAP = 50  # characters
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Free, local sentence-transformers model
COLLECTION_NAME = "policy_documents"


def extract_sections_from_markdown(text: str, filename: str) -> List[Dict[str, str]]:
    """
    Parse markdown text and extract sections with their headings.
    
    Args:
        text: Full markdown document text
        filename: Source filename for metadata
        
    Returns:
        List of dictionaries with 'heading' and 'content' keys
    """
    sections = []
    lines = text.split('\n')
    current_heading = "Introduction"  # Default section for content before first heading
    current_content = []
    
    for line in lines:
        # Check for H2 headings (## Section Title)
        if line.startswith('## '):
            # Save previous section if it has content
            if current_content:
                sections.append({
                    'heading': current_heading,
                    'content': '\n'.join(current_content).strip()
                })
                current_content = []
            # Start new section
            current_heading = line[3:].strip()
        else:
            current_content.append(line)
    
    # Add the last section
    if current_content:
        sections.append({
            'heading': current_heading,
            'content': '\n'.join(current_content).strip()
        })
    
    return sections


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """
    Split text into overlapping chunks of fixed character size.
    
    Args:
        text: Input text to chunk
        chunk_size: Size of each chunk in characters
        overlap: Number of overlapping characters between chunks
        
    Returns:
        List of text chunks
    """
    if not text:
        return []
    
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    
    return chunks


def ingest_documents():
    """
    Main ingestion pipeline:
    1. Discover policy documents
    2. Parse and extract sections
    3. Chunk text
    4. Generate embeddings
    5. Store in ChromaDB with metadata
    """
    
    # Initialize embedding model
    print(f"Loading embedding model: {EMBEDDING_MODEL}")
    embedding_model = SentenceTransformer(EMBEDDING_MODEL)
    
    # Initialize ChromaDB with persistence
    print(f"Initializing ChromaDB with persistence directory: {CHROMA_PERSIST_DIR}")
    chroma_client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    
    # Get or create collection
    collection = chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "Company policy documents for RAG assistant"}
    )
    
    # Discover policy documents
    policies_path = Path(POLICIES_DIR)
    if not policies_path.exists():
        raise FileNotFoundError(f"Policies directory not found: {POLICIES_DIR}")
    
    policy_files = list(policies_path.glob("*.md"))
    print(f"\nDiscovered {len(policy_files)} policy documents:")
    for pf in policy_files:
        print(f"  - {pf.name}")
    
    # Process each document
    total_chunks = 0
    documents_added = 0
    
    for policy_file in policy_files:
        print(f"\nProcessing: {policy_file.name}")
        
        # Read document
        with open(policy_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Extract sections
        sections = extract_sections_from_markdown(text, policy_file.name)
        print(f"  Extracted {len(sections)} sections")
        
        # Process each section
        for section_idx, section in enumerate(sections):
            # Chunk the section content
            chunks = chunk_text(section['content'], CHUNK_SIZE, CHUNK_OVERLAP)
            
            for chunk_idx, chunk in enumerate(chunks):
                # Generate embedding
                embedding = embedding_model.encode(chunk).tolist()
                
                # Create stable document ID
                doc_id = f"{policy_file.stem}_section{section_idx}_chunk{chunk_idx}"
                
                # Store in ChromaDB with metadata
                collection.add(
                    ids=[doc_id],
                    embeddings=[embedding],
                    documents=[chunk],
                    metadatas=[{
                        'filename': policy_file.name,
                        'section': section['heading'],
                        'section_index': str(section_idx),
                        'chunk_index': str(chunk_idx)
                    }]
                )
                
                total_chunks += 1
        
        documents_added += 1
    
    # Verify storage
    count = collection.count()
    print(f"\n{'='*60}")
    print(f"Ingestion Complete!")
    print(f"{'='*60}")
    print(f"Documents processed: {documents_added}")
    print(f"Total chunks created: {total_chunks}")
    print(f"Total chunks in ChromaDB: {count}")
    print(f"ChromaDB persistence directory: {CHROMA_PERSIST_DIR}")
    print(f"Embedding model: {EMBEDDING_MODEL}")
    print(f"Chunk size: {CHUNK_SIZE} characters")
    print(f"Chunk overlap: {CHUNK_OVERLAP} characters")
    print(f"{'='*60}")


if __name__ == "__main__":
    ingest_documents()
