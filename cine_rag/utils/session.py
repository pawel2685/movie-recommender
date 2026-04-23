from __future__ import annotations

import streamlit as st

from config.settings import DEFAULT_TOP_K, DEFAULT_MODEL

_DEFAULTS: dict = {
    "top_k": DEFAULT_TOP_K,
    "model_name": DEFAULT_MODEL,
    "current_question": "",
    "current_result": None,
    "history": [],
    "test_results": [],
}


def init_session() -> None:
    for key, value in _DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_history() -> list[dict]:
    return st.session_state.get("history", [])


def count_hits() -> int:
    return sum(1 for item in get_history() if item.get("found", False))


def get_current_question() -> str:
    return st.session_state.get("current_question", "")


def get_current_result() -> dict | None:
    return st.session_state.get("current_result")


def set_result(question: str, result: dict) -> None:
    st.session_state.current_question = question
    st.session_state.current_result = result
    found = result.get("text") is not None
    st.session_state.history.append({"q": question, "found": found})


def set_quick_question(q: str) -> None:
    st.session_state.current_question = q
    st.session_state.current_result = None


def get_test_results() -> list[dict]:
    return st.session_state.get("test_results", [])


def clear_session() -> None:
    for key, value in _DEFAULTS.items():
        st.session_state[key] = value
