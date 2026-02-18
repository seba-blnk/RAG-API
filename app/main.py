from fastapi import FastAPI

app = FastAPI(title="RAG API", version="0.1.0")

@app.get("/health")
def health_check():
    """Verifica que la API esté corriendo."""
    return {"status": "ok"}