def truncate_text(text: str, max_length: int = 200) -> str:
    """Return text truncated to max_length characters, adding '…' if cut."""
    if len(text) <= max_length:
        return text
    return text[:max_length].rstrip() + "…"


def format_genres(genres: list[str]) -> str:
    """Join a list of genre strings into a comma-separated display string."""
    return ", ".join(genres) if genres else "Brak gatunku"
