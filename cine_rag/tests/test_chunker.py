from pathlib import Path

from langchain_core.documents import Document

from data.chunker import split_documents, _title_from_source


class TestTitleFromSource:
    def test_single_word(self):
        assert _title_from_source("avatar_2009.txt") == "Avatar"

    def test_multi_word(self):
        assert _title_from_source("the_dark_knight_2008.txt") == "The Dark Knight"

    def test_no_year(self):
        assert _title_from_source("inception.txt") == "Inception"


class TestSplitDocuments:
    def _make_doc(self, content: str, source: str = "inception_2010.txt", title: str = "Inception") -> Document:
        return Document(page_content=content, metadata={"source": source, "title": title})

    def test_returns_list_of_documents(self):
        docs = [self._make_doc("A " * 300)]
        chunks = split_documents(docs)
        assert isinstance(chunks, list)
        assert all(isinstance(c, Document) for c in chunks)

    def test_each_chunk_has_chunk_id(self):
        docs = [self._make_doc("word " * 300)]
        chunks = split_documents(docs)
        for chunk in chunks:
            assert "chunk_id" in chunk.metadata
            assert isinstance(chunk.metadata["chunk_id"], int)

    def test_chunk_ids_are_sequential(self):
        docs = [self._make_doc("word " * 300)]
        chunks = split_documents(docs)
        ids = [c.metadata["chunk_id"] for c in chunks]
        assert ids == list(range(len(chunks)))

    def test_each_chunk_has_source(self):
        docs = [self._make_doc("word " * 300)]
        chunks = split_documents(docs)
        for chunk in chunks:
            assert "source" in chunk.metadata
            assert chunk.metadata["source"] == "inception_2010.txt"

    def test_each_chunk_has_title(self):
        docs = [self._make_doc("word " * 300)]
        chunks = split_documents(docs)
        for chunk in chunks:
            assert "title" in chunk.metadata

    def test_title_inferred_from_source_when_missing(self):
        doc = Document(
            page_content="word " * 300,
            metadata={"source": "the_dark_knight_2008.txt"},
        )
        chunks = split_documents([doc])
        for chunk in chunks:
            assert chunk.metadata["title"] == "The Dark Knight"

    def test_short_document_returns_single_chunk(self):
        docs = [self._make_doc("Short content.")]
        chunks = split_documents(docs)
        assert len(chunks) == 1

    def test_empty_input_returns_empty_list(self):
        assert split_documents([]) == []

    def test_multiple_documents_all_chunks_indexed(self):
        docs = [
            self._make_doc("word " * 200, source="a_2000.txt", title="A"),
            self._make_doc("word " * 200, source="b_2001.txt", title="B"),
        ]
        chunks = split_documents(docs)
        ids = [c.metadata["chunk_id"] for c in chunks]
        assert ids == list(range(len(chunks)))
