from __future__ import annotations

import json
from pathlib import Path

import faiss
import numpy as np
from langchain_core.documents import Document
from sentence_transformers import SentenceTransformer

from config.settings import BATCH_SIZE, EMBEDDING_MODEL_NAME, PROCESSED_DIR, VECTOR_STORE_PATH


def build_faiss_index(chunks: list[Document]) -> None:
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    texts = [c.page_content for c in chunks]
    embeddings = model.encode(texts, batch_size=BATCH_SIZE, show_progress_bar=True)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings, dtype="float32"))

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    VECTOR_STORE_PATH.write_bytes(faiss.serialize_index(index).tobytes())

    metadata = [c.metadata for c in chunks]
    with open(PROCESSED_DIR / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
