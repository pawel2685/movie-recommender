import pytest
from unittest.mock import patch

from rag.engine import rag_query
from rag.embeddings import MockEmbeddingModel
from rag.retriever import MockRetriever


@pytest.fixture
def mock_model():
    return MockEmbeddingModel()


@pytest.fixture
def mock_retriever():
    return MockRetriever()


def test_rag_query_returns_dict(mock_model, mock_retriever):
    with (
        patch("rag.engine._load_model", return_value=mock_model),
        patch("rag.engine._load_retriever", return_value=mock_retriever),
        patch("rag.engine.time"),
    ):
        result = rag_query("film akcji")
    assert isinstance(result, dict)
    assert "text" in result
    assert "sources" in result


def test_rag_query_empty_question_returns_none_text(mock_model, mock_retriever):
    with (
        patch("rag.engine._load_model", return_value=mock_model),
        patch("rag.engine._load_retriever", return_value=mock_retriever),
    ):
        result = rag_query("")
    assert result["text"] is None
    assert result["sources"] == []


def test_rag_query_passes_top_k(mock_model, mock_retriever):
    with (
        patch("rag.engine._load_model", return_value=mock_model),
        patch("rag.engine._load_retriever", return_value=mock_retriever),
        patch("rag.engine.time"),
    ):
        result = rag_query("nolan", top_k=2)
    assert isinstance(result, dict)
