from sentence_transformers import SentenceTransformer
import streamlit as st

from config.settings import EMBEDDING_MODEL_NAME


@st.cache_resource
def get_embedding_model() -> SentenceTransformer:
    """Load and cache the sentence-transformers embedding model."""
    return SentenceTransformer(EMBEDDING_MODEL_NAME)
