"""
rag/embeddings.py
Wrapper na model embeddingów (sentence-transformers).
Osoba 2 implementuje tę klasę — UI korzysta z interfejsu, nie z detali.

Instalacja:
    pip install sentence-transformers
"""

from __future__ import annotations
from typing import Protocol
import numpy as np


# ── INTERFEJS (Protocol) ──────────────────────────────────────────────────────
class EmbeddingModel(Protocol):
    def encode(self, texts: list[str]) -> np.ndarray:
        """Zamienia listę tekstów na macierz wektorów."""
        ...


# ── IMPLEMENTACJA (odkomentuj po instalacji sentence-transformers) ─────────────
# from sentence_transformers import SentenceTransformer
#
# class SentenceTransformerModel:
#     def __init__(self, model_name: str):
#         self._model = SentenceTransformer(model_name)
#
#     def encode(self, texts: list[str]) -> np.ndarray:
#         return self._model.encode(texts, normalize_embeddings=True)


# ── MOCK (używany gdy brak sentence-transformers) ─────────────────────────────
class MockEmbeddingModel:
    """
    Zastępczy model do developmentu UI.
    Zwraca losowe wektory jednostkowe zamiast prawdziwych embeddingów.
    """

    DIM = 384  # wymiar zgodny z all-MiniLM-L6-v2

    def encode(self, texts: list[str]) -> np.ndarray:
        rng = np.random.default_rng(seed=hash(texts[0]) % (2**31))
        vecs = rng.standard_normal((len(texts), self.DIM)).astype(np.float32)
        # normalizacja do wektorów jednostkowych
        norms = np.linalg.norm(vecs, axis=1, keepdims=True)
        return vecs / np.where(norms == 0, 1, norms)


# ── FABRYKA ───────────────────────────────────────────────────────────────────
def get_embedding_model(model_name: str) -> EmbeddingModel:
    """
    Zwraca model embeddingów dla podanej nazwy.
    Gdy sentence-transformers nie jest zainstalowany, używa MockEmbeddingModel.
    """
    try:
        from sentence_transformers import SentenceTransformer  # type: ignore

        class _Wrapper:
            def __init__(self, name: str):
                self._m = SentenceTransformer(name)

            def encode(self, texts: list[str]) -> np.ndarray:
                return self._m.encode(texts, normalize_embeddings=True)

        return _Wrapper(model_name)

    except ImportError:
        return MockEmbeddingModel()
