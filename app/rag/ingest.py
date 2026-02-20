from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader
from app.rag.vectorstore import collection
from app.rag.embeddings import embeddings
import uuid

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

def process_pdf(file_bytes: bytes, filename: str) -> int:
    """Extract text from PDF, split into chunks, and store in ChromaDB"""

    #1. Read text from PDF
    reader = PdfReader(file_bytes)
    text=""
    for page in reader.pages:
        text += page.extract_text() or ""

    if not text.strip():
        return 0
    
    #2. Split into chunks
    chunks = text_splitter.split_text(text)

    #3. Generate embeddings for all chunks at once
    vectors = embeddings.embed_documents(chunks)

    #4. Store in ChromaDB
    ids = [str(uuid.uuid4()) for _ in chunks]
    metadatas = [{"source": filename, "chunk": i} for i, _ in enumerate(chunks)]

    collection.add(
        ids=ids,
        embeddings=vectors,
        documents=chunks,
        metadatas=metadatas
    )

    return len(chunks)