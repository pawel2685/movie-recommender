from __future__ import annotations

from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document


def _title_from_filename(filename: str) -> str:
    stem = Path(filename).stem
    parts = stem.rsplit("_", 1)
    name_part = parts[0] if len(parts) == 2 else stem
    return name_part.replace("_", " ").title()


def load_documents(processed_dir: Path) -> list[Document]:
    loader = DirectoryLoader(
        str(processed_dir),
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    documents = loader.load()
    for doc in documents:
        source = Path(doc.metadata.get("source", "")).name
        doc.metadata["source"] = source
        if "title" not in doc.metadata:
            doc.metadata["title"] = _title_from_filename(source)
    return documents
