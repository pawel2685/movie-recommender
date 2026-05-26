"""
api.py
API serwer dla CineRAG — integracja z n8n.

Uruchomienie:
    uvicorn api:app --reload --host 0.0.0.0 --port 8000

Endpointy:
    POST /query  → wykonuje RAG query
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag.engine import rag_query
from config.settings import DEFAULT_TOP_K, DEFAULT_MODEL


# ── MODELE DANYCH ─────────────────────────────────────────────────────────────
class QueryRequest(BaseModel):
    question: str
    top_k: int = DEFAULT_TOP_K
    model_name: str = DEFAULT_MODEL


# ── FASTAPI APP ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="CineRAG API",
    description="API dla systemu rekomendacji filmów opartym na RAG",
    version="1.0.0"
)

# CORS — pozwala na połączenia z n8n (localhost lub inne domeny)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # W produkcji ogranicz do konkretnych domen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── ENDPOINTY ─────────────────────────────────────────────────────────────────
@app.post("/query")
async def query_rag(request: QueryRequest):
    """
    Wykonuje zapytanie RAG na podstawie pytania użytkownika.

    Args:
        request: JSON z pytaniem i opcjami

    Returns:
        JSON z odpowiedzią i źródłami
    """
    try:
        result = rag_query(
            question=request.question,
            top_k=request.top_k,
            model_name=request.model_name
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd podczas przetwarzania zapytania: {str(e)}")


@app.get("/")
async def root():
    """Endpoint zdrowia — sprawdza czy API działa."""
    return {"message": "CineRAG API działa!", "version": "1.0.0"}