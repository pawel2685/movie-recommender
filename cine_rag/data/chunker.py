from __future__ import annotations

from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.settings import CHUNK_OVERLAP, CHUNK_SIZE


def _title_from_source(source: str) -> str:
    stem = Path(source).stem
    parts = stem.rsplit("_", 1)
    name_part = parts[0] if len(parts) == 2 else stem
    return name_part.replace("_", " ").title()


def split_documents(documents: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(documents)
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i
        if "title" not in chunk.metadata:
            chunk.metadata["title"] = _title_from_source(chunk.metadata.get("source", ""))
    return chunks
