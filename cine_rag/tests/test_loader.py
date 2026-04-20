from pathlib import Path

import pytest

from data.loader import load_documents, _title_from_filename


class TestTitleFromFilename:
    def test_simple_slug(self):
        assert _title_from_filename("inception_2010.txt") == "Inception"

    def test_multi_word_slug(self):
        assert _title_from_filename("the_dark_knight_2008.txt") == "The Dark Knight"

    def test_no_year(self):
        assert _title_from_filename("avatar.txt") == "Avatar"


class TestLoadDocuments:
    def _write_txt(self, directory: Path, name: str, content: str) -> None:
        (directory / name).write_text(content, encoding="utf-8")

    def test_loads_all_txt_files(self, tmp_path: Path):
        self._write_txt(tmp_path, "inception_2010.txt", "Tytuł: Inception\nOpis: A dream movie.")
        self._write_txt(tmp_path, "avatar_2009.txt", "Tytuł: Avatar\nOpis: Blue aliens.")
        docs = load_documents(tmp_path)
        assert len(docs) == 2

    def test_page_content_is_not_empty(self, tmp_path: Path):
        self._write_txt(tmp_path, "inception_2010.txt", "Tytuł: Inception\nOpis: A dream movie.")
        docs = load_documents(tmp_path)
        assert all(doc.page_content.strip() for doc in docs)

    def test_metadata_has_source(self, tmp_path: Path):
        self._write_txt(tmp_path, "inception_2010.txt", "Tytuł: Inception")
        docs = load_documents(tmp_path)
        assert docs[0].metadata["source"] == "inception_2010.txt"

    def test_metadata_has_title(self, tmp_path: Path):
        self._write_txt(tmp_path, "inception_2010.txt", "Tytuł: Inception")
        docs = load_documents(tmp_path)
        assert docs[0].metadata["title"] == "Inception"

    def test_multi_word_title_from_filename(self, tmp_path: Path):
        self._write_txt(tmp_path, "the_dark_knight_2008.txt", "Tytuł: The Dark Knight")
        docs = load_documents(tmp_path)
        assert docs[0].metadata["title"] == "The Dark Knight"

    def test_empty_directory_returns_empty_list(self, tmp_path: Path):
        docs = load_documents(tmp_path)
        assert docs == []
