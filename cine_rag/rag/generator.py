def generate_response(query: str, chunks: list[dict]) -> list[dict]:
    """Assemble the final list of movie results from retrieved chunks.

    Currently returns the chunks directly. Replace with an LLM call if
    a generative step is needed.
    """
    if not chunks:
        return []

    # Deduplicate by title and keep the highest-scoring entry
    seen: dict[str, dict] = {}
    for chunk in chunks:
        title = chunk.get("title", "")
        if title not in seen or chunk.get("score", 0) > seen[title].get("score", 0):
            seen[title] = chunk

    return list(seen.values())
