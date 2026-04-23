"""
ui/tabs/tab_base.py
Zakładka "⚙️ Metodologia" — opis techniczny procesu RAG.
"""

from __future__ import annotations
import streamlit as st
from ui.components import question_label


def render() -> None:
    """Renderuje zakładkę Metodologia."""

    st.markdown("""
    <div style="margin-bottom:1.2rem">
        <div class="question-label">Architektura Systemu</div>
        <div style="font-family:'DM Serif Display',serif;font-size:1.8rem;color:#e0d8c8;margin:0.3rem 0 0.6rem">
            Jak działa CineRAG?
        </div>
        <div style="font-size:13px;color:#c08a3a;line-height:1.7">
            Projekt wykorzystuje architekturę <strong>Retrieval-Augmented Generation</strong> (RAG), 
            która łączy przeszukiwanie bazy wektorowej z precyzyjnym dobieraniem kontekstu.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        question_label("1. Indeksowanie (Offline)")
        st.markdown("""
        <div style="font-size:13px; color:#666677; line-height:1.6">
            • <strong>Parsowanie</strong>: Import 4803 filmów z TMDB.<br>
            • <strong>Chunking</strong>: Podział opisów na fragmenty 512 znaków.<br>
            • <strong>Embeddingi</strong>: Model <em>all-MiniLM-L6-v2</em>.<br>
            • <strong>Vector DB</strong>: Indeks FAISS (podobieństwo cosinusowe).
        </div>
        """, unsafe_allow_html=True)

    with col2:
        question_label("2. Wyszukiwanie (Online)")
        st.markdown("""
        <div style="font-size:13px; color:#666677; line-height:1.6">
            • <strong>Encoding</strong>: Wektoryzacja pytania użytkownika.<br>
            • <strong>Similarity</strong>: Szukanie Top-K fragmentów w bazie.<br>
            • <strong>Filtering</strong>: Odrzucanie wyników poniżej progu 0.45.<br>
            • <strong>Presentation</strong>: Wyświetlenie źródeł wraz z ich treścią.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.info("System jest w pełni deterministyczny — odpowiedzi bazują wyłącznie na dostarczonych fragmentach TMDB.")
