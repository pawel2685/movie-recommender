"""
rag/engine.py
Główna funkcja rag_query() — orkiestruje cały pipeline RAG.
To jedyne miejsce, które UI wywołuje.

Przepływ:
    pytanie → embed → search → generate → QueryResult
"""

from __future__ import annotations
import time

from .embeddings import get_embedding_model, EmbeddingModel
from .retriever  import MockRetriever, Retriever
from .generator  import generate_answer, QueryResult
from config.settings import DEFAULT_MODEL, DEFAULT_TOP_K


# ── INICJALIZACJA (raz przy starcie aplikacji) ─────────────────────────────────
# Streamlit cache zapobiega ładowaniu modelu przy każdym rerun.
# Gdy brak runtime Streamlit (testy, uruchomienie bez serwera), używamy lru_cache.
def _build_cache_decorator():
    try:
        from streamlit.runtime import get_instance
        get_instance()
        import streamlit as st
        return st.cache_resource
    except Exception:
        from functools import lru_cache
        return lru_cache(maxsize=None)


_cache = _build_cache_decorator()


@_cache
def _load_model(model_name: str) -> EmbeddingModel:
    """Ładuje i cachuje model embeddingów."""
    return get_embedding_model(model_name)


@_cache
def _load_retriever() -> Retriever:
    """
    Ładuje i cachuje retriever.
    Zamień MockRetriever na FAISSRetriever gdy indeks jest gotowy.
    """
    return MockRetriever()
    # return FAISSRetriever(
    #     index_path=str(INDEX_DIR / "faiss.index"),
    #     metadata=load_metadata(INDEX_DIR / "metadata.json"),
    # )


# ── PUBLICZNY API ─────────────────────────────────────────────────────────────

def rag_query(
    question: str,
    top_k: int    = DEFAULT_TOP_K,
    model_name: str = DEFAULT_MODEL,
) -> dict:
    """
    Wykonuje zapytanie do systemu RAG i zwraca wynik jako słownik.

    Args:
        question:   pytanie użytkownika
        top_k:      ile fragmentów pobrać z bazy wektorowej
        model_name: nazwa modelu embeddingów

    Returns:
        dict z kluczami "text" i "sources" (format oczekiwany przez UI).
        text == None → komunikat "Nie znaleziono informacji".
    """
    if not question.strip():
        return {"text": None, "sources": []}

    model     = _load_model(model_name)
    retriever = _load_retriever()

    # 1. Zamień pytanie na wektor
    query_vector = model.encode([question])[0]

    # 2. Wyszukaj najbliższe fragmenty
    #    MockRetriever używa keyword fallback — prawdziwy retriever używa wektora
    if isinstance(retriever, MockRetriever):
        chunks = retriever.search_by_keyword(question, top_k)
    else:
        chunks = retriever.search(query_vector, top_k)

    # 3. Złóż odpowiedź
    result: QueryResult = generate_answer(question, chunks)

    # Symulacja opóźnienia sieciowego w trybie mock
    if isinstance(retriever, MockRetriever):
        time.sleep(0.8)

    return result.to_dict()
