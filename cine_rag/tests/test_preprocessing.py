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
