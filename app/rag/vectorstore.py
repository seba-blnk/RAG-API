import chromadb
from app.rag.embeddings import embeddings

chroma_client = chromadb.PersistentClient(path="./chroma_data")

collection = chroma_client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space":"cosine"}
)

def reset_collection():
    """Delete all documents and recreate the collection."""
    global collection
    chroma_client.delete_collection("documents")
    collection = chroma_client.get_or_create_collection(
        name="documents",
        metadata={"hnsw:space": "cosine"}
    )

def delete_document(source:str) -> str:
    """Delete all chunks from a specific source file."""
    results = collection.get(where={"source": source})

    if not results["ids"]:
        return 0
    
    collection.delete(ids=results["ids"])
    return len(results["ids"])