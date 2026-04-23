from __future__ import annotations


def fmt_score(score: float) -> str:
    return f"{score:.3f}"


def truncate(text: str, max_length: int = 38) -> str:
    if len(text) <= max_length:
        return text
    return text[:max_length].rstrip() + "…"


def history_icon(found: bool) -> str:
    return "✓" if found else "✗"


def history_color(found: bool, is_active: bool = False) -> str:
    if is_active:
        return "#e0a030"
    return "#336633" if found else "#663333"
