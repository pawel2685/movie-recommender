"""
ui/tabs/tab_main.py
Zakładka "💬 Zapytaj" — główny interfejs wyszukiwania.
"""

from __future__ import annotations
import streamlit as st

from config.constants import QUICK_QUESTIONS
from ui.components import (
    render_answer_card, render_no_results,
    render_source_chips, render_chunk_expander, get_answer_card_html,
    question_label,
)
import utils.session as sess
from rag.engine import rag_retrieve_chunks
from rag.generator import _get_valid_chunks, call_ollama_stream, QueryResult, sanitize_output

T = {
    "Polski": {
        "your_q": "Twoje pytanie",
        "search": "🔍 Szukaj w bazie",
        "clear": "Wyczyść",
        "sample": "Przykładowe pytania",
        "spinner": "⟳ Zamieniam pytanie na wektor · Przeszukuję bazę · Składam odpowiedź…",
    },
    "English": {
        "your_q": "Your question",
        "search": "🔍 Search database",
        "clear": "Clear",
        "sample": "Sample questions",
        "spinner": "⟳ Converting question to vector · Searching database · Composing answer…",
    }
}

def render(top_k: int, model_name: str, show_scores: bool) -> None:
    """
    Renderuje zakładkę Zapytaj.

    Args:
        top_k:       liczba fragmentów do pobrania (z sidebara)
        model_name:  nazwa modelu embeddingów (z sidebara)
        show_scores: czy pokazywać wyniki podobieństwa (z sidebara)
    """
    lang = st.session_state.get("app_language", "Polski")
    t = T[lang]
    # ── POLE PYTANIA ─────────────────────────────────────────────────────────
    question_label(t['your_q'])

    with st.form("query_form", clear_on_submit=False):
        question = st.text_area(
            "",
            value=sess.get_current_question(),
            placeholder="",
            height=85,
            label_visibility="collapsed",
        )
        col_btn1, col_btn2, _ = st.columns([1, 1, 1])
        with col_btn1:
            submitted = st.form_submit_button(t['search'], use_container_width=True)
        with col_btn2:
            cleared = st.form_submit_button(t['clear'], use_container_width=True)

    # ── SZYBKIE PYTANIA ───────────────────────────────────────────────────────
    st.markdown('<div style="margin-top:0.8rem"></div>', unsafe_allow_html=True)
    question_label(t['sample'])
    quick_cols = st.columns(len(QUICK_QUESTIONS))
    for i, (col, q) in enumerate(zip(quick_cols, QUICK_QUESTIONS)):
        with col:
            if st.button(q, key=f"quick_{i}", use_container_width=True):
                sess.set_quick_question(q)
                st.rerun()

    # ── LOGIKA WYSZUKIWANIA ───────────────────────────────────────────────────
    if submitted and question.strip():
        with st.spinner(""):
            st.markdown(
                '<div style="font-family:JetBrains Mono,monospace;font-size:11px;'
                'color:#444455;padding:8px 0">'
                f"{t['spinner']}"
                "</div>",
                unsafe_allow_html=True,
            )
            # 1. Retrieval (Wyszukiwanie fragmentów)
            chunks = rag_retrieve_chunks(question, top_k=top_k, model_name=model_name)
            valid_chunks = _get_valid_chunks(chunks)
            
            if not valid_chunks:
                sess.set_result(question, {"text": None, "sources": []})
                st.rerun()
            
            # 2. Token Streaming (Generowanie odpowiedzi)
            st.markdown("<hr>", unsafe_allow_html=True)
            ans_placeholder = st.empty()
            full_text = ""
            for token in call_ollama_stream(question, valid_chunks):
                full_text += token
                # Sanityzujemy na bieżąco, aby uniknąć migotania kodu HTML w UI
                display_text = sanitize_output(full_text)
                ans_placeholder.markdown(
                    get_answer_card_html(display_text, len(valid_chunks), is_streaming=True),
                    unsafe_allow_html=True
                )
            
            # 3. Finalizacja i zapis do sesji
            # Czyścimy tekst przed zapisem do sesji (usuwamy tagi HTML)
            final_text = sanitize_output(full_text)
            
            # Jeśli model wygenerował tekst o braku wyników (hallucynacja UI) lub odpowiedź jest pusta,
            # traktujemy to jako brak wyników w celu wyświetlenia render_no_results()
            if not final_text.strip() or "Nie znaleziono informacji" in final_text:
                final_text = None

            result_dict = QueryResult(text=final_text, sources=valid_chunks).to_dict()
            sess.set_result(question, result_dict)
        st.rerun()

    if cleared:
        sess.clear_session()
        st.rerun()

    # ── WYŚWIETLANIE ODPOWIEDZI ───────────────────────────────────────────────
    result = sess.get_current_result()
    if result is None:
        return

    st.markdown("<hr>", unsafe_allow_html=True)

    if result["text"] is None:
        render_no_results()
        return

    # Karta odpowiedzi
    render_answer_card(
        text=result["text"],
        num_sources=len(result["sources"]),
        model_name=model_name,
    )

    # Dodaj rozmowę do historii
    sess.add_to_history(question, result["text"])

    # Źródła
    if result["sources"]:
        render_source_chips(result["sources"], show_scores)
        for i, src in enumerate(result["sources"]):
            render_chunk_expander(src, i, show_scores)
