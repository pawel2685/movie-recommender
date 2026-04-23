"""
rag/retriever.py
Wyszukiwanie semantyczne w bazie wektorowej.
Osoba 2 implementuje tę klasę — podłącz FAISS lub ChromaDB.

Instalacja:
    pip install faiss-cpu   # lub faiss-gpu
    pip install chromadb    # alternatywa
"""

from __future__ import annotations
import numpy as np
from dataclasses import dataclass


# ── STRUKTURA WYNIKU ──────────────────────────────────────────────────────────
@dataclass
class RetrievedChunk:
    file:  str    # nazwa pliku źródłowego, np. "inception_2010.txt"
    chunk: int    # numer fragmentu w pliku
    score: float  # cosine similarity (0–1)
    text:  str    # surowy tekst fragmentu


# ── INTERFEJS RETRIEVERA ──────────────────────────────────────────────────────
class Retriever:
    """
    Baza klasy — zaimplementuj search() dla FAISS lub ChromaDB.
    """

    def search(self, query_vector: np.ndarray, top_k: int) -> list[RetrievedChunk]:
        raise NotImplementedError


# ── MOCK RETRIEVER ────────────────────────────────────────────────────────────
class MockRetriever(Retriever):
    """
    Zastępczy retriever — zwraca predefiniowane wyniki dla wybranych słów kluczowych.
    Używany podczas developmentu UI zanim Osoba 2 dostarczy prawdziwy indeks.
    """

    _MOCK_DB: dict[str, list[RetrievedChunk]] = {
        "nolan": [
            RetrievedChunk("interstellar_2014.txt", 3, 0.94,
                "Interstellar (2014) reż. Christopher Nolan. Gatunek: Sci-Fi, Dramat. "
                "Ocena: 8.6/10. Obsada: Matthew McConaughey, Anne Hathaway, Jessica Chastain."),
            RetrievedChunk("inception_2010.txt", 1, 0.91,
                "Inception (2010) reż. Christopher Nolan. Gatunek: Thriller, Sci-Fi. "
                "Dom Cobb to złodziej kradnący sekrety z podświadomości śpiących ludzi."),
            RetrievedChunk("dark_knight_2008.txt", 2, 0.87,
                "The Dark Knight (2008) reż. Christopher Nolan. "
                "Batman podejmuje walkę z Jokerem — anarchistycznym przestępcą."),
        ],
        "interstellar": [],   # przekierowane do "nolan"
        "inception":    [],
    }

    def search(self, query_vector: np.ndarray, top_k: int) -> list[RetrievedChunk]:
        # MockRetriever ignoruje query_vector — klucz przekazywany jest z engine.py
        return []

    def search_by_keyword(self, keyword: str, top_k: int) -> list[RetrievedChunk]:
        """Wyszukiwanie po słowie kluczowym (tylko dla MockRetriever)."""
        for key, chunks in self._MOCK_DB.items():
            if key in keyword.lower():
                return chunks[:top_k]
        return []


# ── FAISS RETRIEVER (szkielet) ────────────────────────────────────────────────
# class FAISSRetriever(Retriever):
#     def __init__(self, index_path: str, metadata: list[dict]):
#         import faiss
#         self._index    = faiss.read_index(index_path)
#         self._metadata = metadata   # lista słowników: {file, chunk, text}
#
#     def search(self, query_vector: np.ndarray, top_k: int) -> list[RetrievedChunk]:
#         scores, indices = self._index.search(
#             query_vector.reshape(1, -1).astype("float32"), top_k
#         )
#         results = []
#         for score, idx in zip(scores[0], indices[0]):
#             if idx == -1:
#                 continue
#             meta = self._metadata[idx]
#             results.append(RetrievedChunk(
#                 file=meta["file"], chunk=meta["chunk"],
#                 score=float(score), text=meta["text"]
#             ))
#         return results
