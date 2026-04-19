import streamlit as st

from config.settings import TOP_K_DEFAULT, EMBEDDING_MODEL_NAME


def init_session_state() -> None:
    """Initialise all session_state keys with default values if not already set."""
    defaults: dict = {
        "top_k": TOP_K_DEFAULT,
        "embedding_model": EMBEDDING_MODEL_NAME,
        "last_query": "",
        "last_results": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
