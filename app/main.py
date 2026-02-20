from io import BytesIO
from fastapi import FastAPI, UploadFile
from app.models.schemas import QuestionRequest, QuestionResponse
from app.rag.chain import ask
from app.rag.ingest import process_pdf
from app.rag import vectorstore

app = FastAPI(title="RAG API", version="0.1.0")

@app.get("/health")
def health_check():
    """Check if the API is running."""
    return {"status": "ok"}

@app.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):
    """Receive a question and respond using RAG"""
    result = ask(request.question)
    return QuestionResponse(
        answer=result["answer"],
        context=result["context"]
    )

@app.post("/upload")
async def upload_document(file: UploadFile):
    """Upload a PDF document to be processed and stored."""
    contents = await file.read()
    file_stream = BytesIO(contents)

    chunks_count = process_pdf(file_stream, file.filename)

    return {
        "filename": file.filename,
        "chunks": chunks_count,
        "message": f"Document processed into {chunks_count} chunks."
    }

@app.get("/documents")
def list_documents():
    """List all documents stored in the vector store."""
    data = vectorstore.collection.get()

    if not data["ids"]:
        return{
            "total_chunks": 0,
            "sources": []
        }

    sources = set()
    for metadata in data["metadatas"]:
        sources.add(metadata["source"])
    
    return {
        "total_chunks": len(data["ids"]),
        "sources": list(sources)
    }

@app.delete("/documents")
def delete_documents():
    """Delete all documents from the vector store."""
    vectorstore.reset_collection()
    return {"message": "All documents deleted."}

@app.delete("/documents/source")
def delete_document(filename: str):
    """Delete al chunks from a specific source file."""
    deleted = vectorstore.delete_document(filename)

    if deleted == 0:
        return {"message": f"No documents found with source '{filename}'"}
    
    return {"message": f"Deleted {deleted} chunks from '{filename}'."}