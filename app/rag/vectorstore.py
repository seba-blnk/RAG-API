import chromadb
from app.rag.embeddings import embeddings

chroma_client = chromadb.PersistentClient(path="./chroma_data")

collection = chroma_client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space":"cosine"}
)