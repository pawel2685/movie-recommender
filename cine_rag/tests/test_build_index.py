from unittest.mock import MagicMock, call, patch

import pandas as pd
import pytest
from langchain_core.documents import Document

from data.build_index import main


@pytest.fixture()
def mock_pipeline(tmp_path):
    dummy_df = pd.DataFrame({
        "title": ["Inception"],
        "overview": ["A dream movie."],
        "genres": [["Sci-Fi"]],
        "cast": [["DiCaprio"]],
        "director": ["Nolan"],
        "vote_average": [8.8],
        "release_year": [2010],
    })
    dummy_docs = [Document(page_content="doc", metadata={"source": "inception_2010.txt", "title": "Inception"})]
    dummy_chunks = [Document(page_content="chunk", metadata={"source": "inception_2010.txt", "chunk_id": 0, "title": "Inception"})]

    with (
        patch("data.build_index.build_clean_dataframe", return_value=dummy_df) as mock_build,
        patch("data.build_index.save_documents_as_txt") as mock_save,
        patch("data.build_index.load_documents", return_value=dummy_docs) as mock_load,
        patch("data.build_index.split_documents", return_value=dummy_chunks) as mock_split,
        patch("data.build_index.export_chunks_to_json") as mock_export,
    ):
        yield {
            "build_clean_dataframe": mock_build,
            "save_documents_as_txt": mock_save,
            "load_documents": mock_load,
            "split_documents": mock_split,
            "export_chunks_to_json": mock_export,
        }


class TestMain:
    def test_all_stages_called(self, mock_pipeline):
        main()
        for mock in mock_pipeline.values():
            mock.assert_called_once()

    def test_build_clean_dataframe_called_with_raw_dir(self, mock_pipeline):
        from config.settings import RAW_DIR
        main()
        mock_pipeline["build_clean_dataframe"].assert_called_once_with(RAW_DIR)

    def test_save_documents_as_txt_receives_dataframe(self, mock_pipeline):
        main()
        args, _ = mock_pipeline["save_documents_as_txt"].call_args
        assert isinstance(args[0], pd.DataFrame)

    def test_load_documents_called_with_processed_dir(self, mock_pipeline):
        from config.settings import PROCESSED_DIR
        main()
        mock_pipeline["load_documents"].assert_called_once_with(PROCESSED_DIR)

    def test_split_documents_receives_loaded_docs(self, mock_pipeline):
        main()
        args, _ = mock_pipeline["split_documents"].call_args
        assert isinstance(args[0], list)
        assert all(isinstance(d, Document) for d in args[0])

    def test_export_chunks_to_json_receives_chunks(self, mock_pipeline):
        main()
        args, _ = mock_pipeline["export_chunks_to_json"].call_args
        assert isinstance(args[0], list)
        assert all(isinstance(c, Document) for c in args[0])

    def test_stages_called_in_order(self, mock_pipeline):
        manager = MagicMock()
        manager.attach_mock(mock_pipeline["build_clean_dataframe"], "build_clean_dataframe")
        manager.attach_mock(mock_pipeline["save_documents_as_txt"], "save_documents_as_txt")
        manager.attach_mock(mock_pipeline["load_documents"], "load_documents")
        manager.attach_mock(mock_pipeline["split_documents"], "split_documents")
        manager.attach_mock(mock_pipeline["export_chunks_to_json"], "export_chunks_to_json")

        main()

        call_names = [c[0] for c in manager.mock_calls]
        assert call_names.index("build_clean_dataframe") < call_names.index("save_documents_as_txt")
        assert call_names.index("save_documents_as_txt") < call_names.index("load_documents")
        assert call_names.index("load_documents") < call_names.index("split_documents")
        assert call_names.index("split_documents") < call_names.index("export_chunks_to_json")
