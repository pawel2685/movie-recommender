import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pytest
from langchain_core.documents import Document

from data.indexer import build_faiss_index


def _make_chunks(n: int = 3) -> list[Document]:
    return [
        Document(
            page_content=f"Content of chunk {i}",
            metadata={"source": f"movie_{i}.txt", "chunk_id": i, "title": f"Movie {i}"},
        )
        for i in range(n)
    ]


@pytest.fixture()
def mock_sentence_transformer():
    with patch("data.indexer.SentenceTransformer") as MockST:
        instance = MagicMock()
        instance.encode.return_value = np.random.rand(3, 384).astype("float32")
        MockST.return_value = instance
        yield instance


class TestBuildFaissIndex:
    def test_creates_faiss_index_file(self, tmp_path: Path, mock_sentence_transformer, monkeypatch):
        monkeypatch.setattr("data.indexer.PROCESSED_DIR", tmp_path)
        monkeypatch.setattr("data.indexer.VECTOR_STORE_PATH", tmp_path / "faiss.index")

        chunks = _make_chunks(3)
        mock_sentence_transformer.encode.return_value = np.random.rand(3, 384).astype("float32")

        build_faiss_index(chunks)

        assert (tmp_path / "faiss.index").exists()

    def test_creates_metadata_json_file(self, tmp_path: Path, mock_sentence_transformer, monkeypatch):
        monkeypatch.setattr("data.indexer.PROCESSED_DIR", tmp_path)
        monkeypatch.setattr("data.indexer.VECTOR_STORE_PATH", tmp_path / "faiss.index")

        chunks = _make_chunks(3)
        mock_sentence_transformer.encode.return_value = np.random.rand(3, 384).astype("float32")

        build_faiss_index(chunks)

        assert (tmp_path / "metadata.json").exists()

    def test_metadata_json_contains_all_chunks(self, tmp_path: Path, mock_sentence_transformer, monkeypatch):
        monkeypatch.setattr("data.indexer.PROCESSED_DIR", tmp_path)
        monkeypatch.setattr("data.indexer.VECTOR_STORE_PATH", tmp_path / "faiss.index")

        chunks = _make_chunks(3)
        mock_sentence_transformer.encode.return_value = np.random.rand(3, 384).astype("float32")

        build_faiss_index(chunks)

        with open(tmp_path / "metadata.json", encoding="utf-8") as f:
            metadata = json.load(f)
        assert len(metadata) == 3

    def test_metadata_json_has_required_fields(self, tmp_path: Path, mock_sentence_transformer, monkeypatch):
        monkeypatch.setattr("data.indexer.PROCESSED_DIR", tmp_path)
        monkeypatch.setattr("data.indexer.VECTOR_STORE_PATH", tmp_path / "faiss.index")

        chunks = _make_chunks(3)
        mock_sentence_transformer.encode.return_value = np.random.rand(3, 384).astype("float32")

        build_faiss_index(chunks)

        with open(tmp_path / "metadata.json", encoding="utf-8") as f:
            metadata = json.load(f)
        for entry in metadata:
            assert "source" in entry
            assert "chunk_id" in entry
            assert "title" in entry

    def test_faiss_index_has_correct_vector_count(self, tmp_path: Path, mock_sentence_transformer, monkeypatch):
        monkeypatch.setattr("data.indexer.PROCESSED_DIR", tmp_path)
        monkeypatch.setattr("data.indexer.VECTOR_STORE_PATH", tmp_path / "faiss.index")

        chunks = _make_chunks(3)
        mock_sentence_transformer.encode.return_value = np.random.rand(3, 384).astype("float32")

        build_faiss_index(chunks)

        import faiss as faiss_lib
        index = faiss_lib.read_index(str(tmp_path / "faiss.index"))
        assert index.ntotal == 3

    def test_creates_processed_dir_if_missing(self, tmp_path: Path, mock_sentence_transformer, monkeypatch):
        target = tmp_path / "new_processed"
        monkeypatch.setattr("data.indexer.PROCESSED_DIR", target)
        monkeypatch.setattr("data.indexer.VECTOR_STORE_PATH", target / "faiss.index")

        chunks = _make_chunks(2)
        mock_sentence_transformer.encode.return_value = np.random.rand(2, 384).astype("float32")

        build_faiss_index(chunks)

        assert target.is_dir()
