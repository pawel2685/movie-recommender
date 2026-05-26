"""
ui/tabs/tab_base.py
Zakładka "⚙️ Metodologia" — opis techniczny procesu RAG.
"""

from __future__ import annotations
import streamlit as st
from ui.components import question_label

T = {
    "Polski": {
        "arch_label": "Architektura Systemu",
        "how_it_works": "Jak działa CineRAG?",
        "intro_desc": "Projekt wykorzystuje architekturę <strong>Retrieval-Augmented Generation</strong> (RAG), która łączy przeszukiwanie bazy wektorowej z precyzyjnym dobieraniem kontekstu.",
        "indexing_label": "1. Indeksowanie (Offline)",
        "indexing_details": "• <strong>Parsowanie</strong>: Import 4803 filmów z TMDB.<br>• <strong>Chunking</strong>: Podział opisów na fragmenty 512 znaków.<br>• <strong>Embeddingi</strong>: Model <em>all-MiniLM-L6-v2</em>.<br>• <strong>Vector DB</strong>: Indeks FAISS (podobieństwo cosinusowe).",
        "search_label": "2. Wyszukiwanie (Online)",
        "search_details": "• <strong>Encoding</strong>: Wektoryzacja pytania użytkownika.<br>• <strong>Similarity</strong>: Szukanie Top-K fragmentów w bazie.<br>• <strong>Filtering</strong>: Odrzucanie wyników poniżej progu 0.45.<br>• <strong>Presentation</strong>: Wyświetlenie źródeł wraz z ich treścią.",
        "info_msg": "System jest w pełni deterministyczny — odpowiedzi bazują wyłącznie na dostarczonych fragmentach TMDB."
    },
    "English": {
        "arch_label": "System Architecture",
        "how_it_works": "How CineRAG Works",
        "intro_desc": "The project uses the <strong>Retrieval-Augmented Generation</strong> (RAG) architecture, which combines vector database searching with precise context selection.",
        "indexing_label": "1. Indexing (Offline)",
        "indexing_details": "• <strong>Parsing</strong>: Importing 4803 movies from TMDB.<br>• <strong>Chunking</strong>: Splitting descriptions into 512-character fragments.<br>• <strong>Embeddings</strong>: <em>all-MiniLM-L6-v2</em> model.<br>• <strong>Vector DB</strong>: FAISS index (cosine similarity).",
        "search_label": "2. Search (Online)",
        "search_details": "• <strong>Encoding</strong>: Vectorizing the user question.<br>• <strong>Similarity</strong>: Searching for Top-K fragments in the database.<br>• <strong>Filtering</strong>: Rejecting results below a 0.45 threshold.<br>• <strong>Presentation</strong>: Displaying sources along with their content.",
        "info_msg": "The system is fully deterministic — answers are based solely on the provided TMDB fragments."
    }
}

def render() -> None:
    """Renderuje zakładkę Metodologia."""
    lang = st.session_state.get("app_language", "Polski")
    t = T[lang]

    st.markdown(f"""
    <div style="margin-bottom:1.2rem">
        <div class="question-label">{t['arch_label']}</div>
        <div style="font-family:'DM Serif Display',serif;font-size:1.8rem;color:#e0d8c8;margin:0.3rem 0 0.6rem">
            {t['how_it_works']}
        </div>
        <div style="font-size:13px;color:#c08a3a;line-height:1.7">
            {t['intro_desc']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        question_label(t['indexing_label'])
        st.markdown(f"""
        <div style="font-size:13px; color:#666677; line-height:1.6">
            {t['indexing_details']}
        </div>
        """, unsafe_allow_html=True)

    with col2:
        question_label(t['search_label'])
        st.markdown(f"""
        <div style="font-size:13px; color:#666677; line-height:1.6">
            {t['search_details']}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.info(t['info_msg'])
