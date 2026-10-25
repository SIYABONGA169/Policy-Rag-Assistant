"""
Quick verification script to check ChromaDB ingestion results
"""
import chromadb

CHROMA_PERSIST_DIR = ".chroma"
COLLECTION_NAME = "policy_documents"

# Connect to ChromaDB
client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
collection = client.get_collection(name=COLLECTION_NAME)

# Get collection info
count = collection.count()
print(f"Total chunks in ChromaDB: {count}")

# Get a sample chunk to verify metadata
if count > 0:
    sample = collection.get(limit=1, include=['metadatas', 'documents'])
    print(f"\nSample chunk metadata:")
    print(f"  ID: {sample['ids'][0]}")
    print(f"  Metadata: {sample['metadatas'][0]}")
    print(f"  Document preview: {sample['documents'][0][:100]}...")
    
    # Check for unique documents
    all_metadata = collection.get(include=['metadatas'])['metadatas']
    unique_files = set(m['filename'] for m in all_metadata)
    print(f"\nUnique source documents: {len(unique_files)}")
    for filename in sorted(unique_files):
        print(f"  - {filename}")
