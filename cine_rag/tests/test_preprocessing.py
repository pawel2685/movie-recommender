import json
from pathlib import Path

import pandas as pd
import pytest

from data.preprocessing import (
    build_clean_dataframe,
    clean_text,
    extract_cast,
    extract_director,
    extract_genres,
    merge_datasets,
    save_documents_as_txt,
)


def _to_json(data: list) -> str:
    return json.dumps(data)


class TestExtractGenres:
    def test_returns_names(self):
        raw = _to_json([{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}])
        assert extract_genres(raw) == ["Action", "Adventure"]

    def test_caps_at_five(self):
        raw = _to_json([{"id": i, "name": f"G{i}"} for i in range(10)])
        assert len(extract_genres(raw)) == 5

    def test_empty_string_returns_empty_list(self):
        assert extract_genres("") == []

    def test_invalid_json_returns_empty_list(self):
        assert extract_genres("not json") == []


class TestExtractCast:
    def test_returns_names_sorted_by_order(self):
        raw = _to_json([
            {"name": "Bob", "order": 2},
            {"name": "Alice", "order": 0},
            {"name": "Carol", "order": 1},
        ])
        assert extract_cast(raw, top_n=3) == ["Alice", "Carol", "Bob"]

    def test_respects_top_n(self):
        raw = _to_json([{"name": f"Actor{i}", "order": i} for i in range(10)])
        assert len(extract_cast(raw, top_n=3)) == 3

    def test_default_top_n_is_five(self):
        raw = _to_json([{"name": f"Actor{i}", "order": i} for i in range(10)])
        assert len(extract_cast(raw)) == 5

    def test_empty_string_returns_empty_list(self):
        assert extract_cast("") == []


class TestExtractDirector:
    def test_finds_director(self):
        raw = _to_json([
            {"name": "John Doe", "job": "Producer"},
            {"name": "Jane Smith", "job": "Director"},
        ])
        assert extract_director(raw) == "Jane Smith"

    def test_returns_empty_string_when_no_director(self):
        raw = _to_json([{"name": "John Doe", "job": "Producer"}])
        assert extract_director(raw) == ""

    def test_returns_first_director_when_multiple(self):
        raw = _to_json([
            {"name": "First Director", "job": "Director"},
            {"name": "Second Director", "job": "Director"},
        ])
        assert extract_director(raw) == "First Director"

    def test_empty_string_returns_empty_string(self):
        assert extract_director("") == ""


class TestCleanText:
    def test_removes_special_characters(self):
        assert "@#$" not in clean_text("Hello @#$ World")

    def test_normalizes_whitespace(self):
        assert clean_text("too   many    spaces") == "too many spaces"

    def test_strips_leading_trailing_whitespace(self):
        assert clean_text("  hello  ") == "hello"

    def test_preserves_basic_punctuation(self):
        result = clean_text("Hello, world! How are you?")
        assert "," in result
        assert "!" in result
        assert "?" in result

    def test_empty_string_returns_empty_string(self):
        assert clean_text("") == ""


class TestMergeDatasets:
    def test_merges_on_id(self):
        movies = pd.DataFrame({"id": [1, 2], "title": ["A", "B"]})
        credits = pd.DataFrame({"movie_id": [1, 2], "cast": ["[]", "[]"]})
        result = merge_datasets(movies, credits)
        assert len(result) == 2
        assert "title" in result.columns
        assert "cast" in result.columns

    def test_inner_join_drops_unmatched_rows(self):
        movies = pd.DataFrame({"id": [1, 2, 3], "title": ["A", "B", "C"]})
        credits = pd.DataFrame({"movie_id": [1, 2], "cast": ["[]", "[]"]})
        result = merge_datasets(movies, credits)
        assert len(result) == 2


class TestBuildCleanDataframe:
    def test_required_columns_present(self, tmp_path: Path):
        movies = pd.DataFrame({
            "id": [1],
            "title": ["Inception"],
            "overview": ["A dream movie."],
            "genres": [_to_json([{"id": 878, "name": "Sci-Fi"}])],
            "keywords": [_to_json([])],
            "release_date": ["2010-07-16"],
            "vote_average": [8.8],
        })
        credits = pd.DataFrame({
            "movie_id": [1],
            "cast": [_to_json([{"name": "DiCaprio", "order": 0}])],
            "crew": [_to_json([{"name": "Nolan", "job": "Director"}])],
        })
        movies.to_csv(tmp_path / "tmdb_5000_movies.csv", index=False)
        credits.to_csv(tmp_path / "tmdb_5000_credits.csv", index=False)

        df = build_clean_dataframe(tmp_path)

        required = {"title", "overview", "genres", "cast", "director", "vote_average", "release_year"}
        assert required.issubset(set(df.columns))

    def test_overview_has_no_nulls(self, tmp_path: Path):
        movies = pd.DataFrame({
            "id": [1],
            "title": ["Unknown"],
            "overview": [None],
            "genres": [_to_json([])],
            "keywords": [_to_json([])],
            "release_date": [None],
            "vote_average": [0.0],
        })
        credits = pd.DataFrame({
            "movie_id": [1],
            "cast": [_to_json([])],
            "crew": [_to_json([])],
        })
        movies.to_csv(tmp_path / "tmdb_5000_movies.csv", index=False)
        credits.to_csv(tmp_path / "tmdb_5000_credits.csv", index=False)

        df = build_clean_dataframe(tmp_path)

        assert df["overview"].isnull().sum() == 0


class TestSaveDocumentsAsTxt:
    def _make_df(self) -> pd.DataFrame:
        return pd.DataFrame({
            "title": ["Inception", "The Dark Knight"],
            "release_year": [2010, 2008],
            "genres": [["Sci-Fi", "Action"], ["Action", "Crime"]],
            "director": ["Christopher Nolan", "Christopher Nolan"],
            "cast": [["DiCaprio", "Hardy"], ["Bale", "Ledger"]],
            "vote_average": [8.8, 9.0],
            "overview": ["A dream heist movie.", "A superhero crime thriller."],
        })

    def test_creates_one_file_per_row(self, tmp_path: Path):
        df = self._make_df()
        save_documents_as_txt(df, tmp_path)
        txt_files = list(tmp_path.glob("*.txt"))
        assert len(txt_files) == 2

    def test_filename_is_slugified(self, tmp_path: Path):
        df = self._make_df()
        save_documents_as_txt(df, tmp_path)
        names = {f.name for f in tmp_path.glob("*.txt")}
        assert "inception_2010.txt" in names
        assert "the_dark_knight_2008.txt" in names

    def test_file_contains_required_fields(self, tmp_path: Path):
        df = self._make_df()
        save_documents_as_txt(df, tmp_path)
        content = (tmp_path / "inception_2010.txt").read_text(encoding="utf-8")
        assert "Tytuł: Inception" in content
        assert "Rok: 2010" in content
        assert "Gatunki: Sci-Fi, Action" in content
        assert "Reżyser: Christopher Nolan" in content
        assert "Obsada: DiCaprio, Hardy" in content
        assert "8.8/10" in content
        assert "A dream heist movie." in content

    def test_creates_directory_if_not_exists(self, tmp_path: Path):
        target = tmp_path / "new_subdir"
        df = self._make_df()
        save_documents_as_txt(df, target)
        assert target.is_dir()
        assert len(list(target.glob("*.txt"))) == 2
