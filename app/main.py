from fastapi import FastAPI
from app.models.schemas import QuestionRequest, QuestionResponse

app = FastAPI(title="RAG API", version="0.1.0")

@app.get("/health")
def health_check():
    """Verifica que la API esté corriendo."""
    return {"status": "ok"}

@app.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):
    """Recibe un pregunta y responde usando RAG"""
    return QuestionResponse(
        answer=f"Placeholder: pregunta '{request.question}'",
        context=["contexto.pdf - chunk 1"]
    )