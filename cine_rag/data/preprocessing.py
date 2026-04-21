from __future__ import annotations

import ast
import re
from pathlib import Path

import pandas as pd


def load_raw_data(raw_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    movies = pd.read_csv(raw_dir / "tmdb_5000_movies.csv")
    credits = pd.read_csv(raw_dir / "tmdb_5000_credits.csv")
    return movies, credits


def merge_datasets(movies_df: pd.DataFrame, credits_df: pd.DataFrame) -> pd.DataFrame:
    credits_clean = credits_df.drop(columns=["title"], errors="ignore")
    return movies_df.merge(credits_clean, left_on="id", right_on="movie_id", how="inner")


def _safe_parse(value: str) -> list:
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return []


def extract_genres(genres_json: str) -> list[str]:
    parsed = _safe_parse(genres_json)
    return [item["name"] for item in parsed if "name" in item][:5]


def extract_cast(cast_json: str, top_n: int = 5) -> list[str]:
    parsed = _safe_parse(cast_json)
    sorted_cast = sorted(parsed, key=lambda x: x.get("order", 999))
    return [member["name"] for member in sorted_cast if "name" in member][:top_n]


def extract_director(crew_json: str) -> str:
    parsed = _safe_parse(crew_json)
    for member in parsed:
        if member.get("job") == "Director":
            return member.get("name", "")
    return ""


def clean_text(text: str) -> str:
    text = re.sub(r"[^\w\s.,!?;:()\-']", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def build_clean_dataframe(raw_dir: Path) -> pd.DataFrame:
    movies, credits = load_raw_data(raw_dir)
    merged = merge_datasets(movies, credits)

    merged["release_year"] = pd.to_datetime(
        merged["release_date"], errors="coerce"
    ).dt.year.fillna(0).astype(int)

    merged["genres"] = merged["genres"].apply(extract_genres)
    merged["cast"] = merged["cast"].apply(extract_cast)
    merged["director"] = merged["crew"].apply(extract_director)
    merged["overview"] = merged["overview"].fillna("").apply(clean_text)

    columns = ["title", "overview", "genres", "cast", "director", "vote_average", "release_year"]
    return merged[columns].reset_index(drop=True)


def _slugify(title: str, year: int) -> str:
    slug = title.lower()
    slug = re.sub(r"[^\w\s]", "", slug)
    slug = re.sub(r"\s+", "_", slug).strip("_")
    return f"{slug}_{year}.txt"


def save_documents_as_txt(df: pd.DataFrame, processed_dir: Path) -> None:
    processed_dir.mkdir(parents=True, exist_ok=True)
    for _, row in df.iterrows():
        genres_joined = ", ".join(row["genres"]) if row["genres"] else ""
        cast_joined = ", ".join(row["cast"]) if row["cast"] else ""
        content = (
            f"Tytuł: {row['title']}\n"
            f"Rok: {row['release_year']}\n"
            f"Gatunki: {genres_joined}\n"
            f"Reżyser: {row['director']}\n"
            f"Obsada: {cast_joined}\n"
            f"Ocena: {row['vote_average']}/10\n"
            f"\nOpis:\n{row['overview']}\n"
        )
        filename = _slugify(str(row["title"]), int(row["release_year"]))
        (processed_dir / filename).write_text(content, encoding="utf-8")
