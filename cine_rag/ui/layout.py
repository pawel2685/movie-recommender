import streamlit as st


def render_header():
    st.title("🎬 CineRAG")
    st.caption("System rekomendacji filmów oparty na RAG")


def render_sidebar():
    with st.sidebar:
        st.header("Ustawienia")
        st.slider("Liczba wyników (top_k)", min_value=1, max_value=20, value=5, key="top_k")
        st.selectbox("Model embeddingów", options=["all-MiniLM-L6-v2", "paraphrase-multilingual-MiniLM-L12-v2"], key="embedding_model")
