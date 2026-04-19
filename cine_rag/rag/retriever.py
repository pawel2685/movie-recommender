import numpy as np

from config.settings import VECTOR_STORE_PATH, TOP_K_DEFAULT

# Lazy-loaded index – populated by build_index() or loaded from disk
_index = None
_metadata: list[dict] = []


def build_index(embeddings: np.ndarray, metadata: list[dict]) -> None:
    """Build a FAISS index from pre-computed embeddings."""
    import faiss

    global _index, _metadata
    dim = embeddings.shape[1]
    _index = faiss.IndexFlatL2(dim)
    _index.add(embeddings.astype(np.float32))
    _metadata = metadata


def load_index() -> None:
    """Load a persisted FAISS index from disk."""
    import faiss

    global _index
    _index = faiss.read_index(str(VECTOR_STORE_PATH))


def retrieve(query_embedding: np.ndarray, top_k: int = TOP_K_DEFAULT) -> list[dict]:
    """Return the top_k most similar chunks for the given query embedding."""
    if _index is None:
        return []

    distances, indices = _index.search(
        query_embedding.reshape(1, -1).astype(np.float32), top_k
    )
    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx == -1:
            continue
        entry = dict(_metadata[idx])
        entry["score"] = float(1 / (1 + dist))
        results.append(entry)
    return results
