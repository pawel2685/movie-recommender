import pytest
from unittest.mock import patch, MagicMock

from rag.engine import rag_query


@pytest.fixture
def mock_model():
    model = MagicMock()
    model.encode.return_value = [0.1] * 384
    return model


def test_rag_query_returns_list(mock_model):
    with (
        patch("rag.engine.get_embedding_model", return_value=mock_model),
        patch("rag.engine.retrieve", return_value=[]),
        patch("rag.engine.generate_response", return_value=[]),
    ):
        result = rag_query("film akcji")
    assert isinstance(result, list)


def test_rag_query_passes_top_k(mock_model):
    with (
        patch("rag.engine.get_embedding_model", return_value=mock_model),
        patch("rag.engine.retrieve", return_value=[]) as mock_retrieve,
        patch("rag.engine.generate_response", return_value=[]),
    ):
        rag_query("komedia romantyczna", top_k=3)
    mock_retrieve.assert_called_once()
    _, kwargs = mock_retrieve.call_args
    assert kwargs.get("top_k") == 3
