"""
rag/engine.py
Główna funkcja rag_query() — orkiestruje cały pipeline RAG.
To jedyne miejsce, które UI wywołuje.

Przepływ:
    pytanie → embed → search → generate → QueryResult
"""

from __future__ import annotations
import time
import hashlib

from .embeddings import get_embedding_model, EmbeddingModel
from .retriever import MockRetriever, Retriever, QdrantRetriever
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
    return QdrantRetriever()
    # return FAISSRetriever(...)

def rag_retrieve_chunks(
    question: str,
    top_k: int    = DEFAULT_TOP_K,
    model_name: str = DEFAULT_MODEL,
):
    """Wykonuje tylko etap wyszukiwania fragmentów z bazy."""
    if not question.strip():
        return []

    model     = _load_model(model_name)
    retriever = _load_retriever()

    query_vector = model.encode([question])[0]

    if isinstance(retriever, MockRetriever):
        raw_chunks = retriever.search_by_keyword(question, top_k * 2)
    else:
        raw_chunks = retriever.search(query_vector, top_k * 2)

    unique_chunks = []
    seen_contents = set()
    for c in raw_chunks:
        content_hash = hashlib.md5(c.text.strip().encode('utf-8')).hexdigest()
        if content_hash not in seen_contents:
            unique_chunks.append(c)
            seen_contents.add(content_hash)
        if len(unique_chunks) >= top_k:
            break
    return unique_chunks

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
    unique_chunks = rag_retrieve_chunks(question, top_k, model_name)
    result: QueryResult = generate_answer(question, unique_chunks)
    return result.to_dict()
