"""
ui/tabs/tab_main.py
Zakładka "💬 Zapytaj" — główny interfejs wyszukiwania.
"""

from __future__ import annotations
import streamlit as st

from config.constants import QUICK_QUESTIONS
from ui.components import (
    render_answer_card, render_no_results,
    render_source_chips, render_chunk_expander,
    question_label,
)
import utils.session as sess
from rag import rag_query


def render(top_k: int, model_name: str, show_scores: bool) -> None:
    """
    Renderuje zakładkę Zapytaj.

    Args:
        top_k:       liczba fragmentów do pobrania (z sidebara)
        model_name:  nazwa modelu embeddingów (z sidebara)
        show_scores: czy pokazywać wyniki podobieństwa (z sidebara)
    """
    # ── POLE PYTANIA ─────────────────────────────────────────────────────────
    question_label("Twoje pytanie")

    with st.form("query_form", clear_on_submit=False):
        question = st.text_area(
            "",
            value=sess.get_current_question(),
            placeholder="np. Jakie filmy wyreżyserował Christopher Nolan?",
            height=150,
            label_visibility="collapsed",
        )
        col_btn1, col_btn2, _ = st.columns([1, 1, 1])
        with col_btn1:
            submitted = st.form_submit_button("🔍  Szukaj w bazie", use_container_width=True)
        with col_btn2:
            cleared = st.form_submit_button("Wyczyść", use_container_width=True)

    # ── SZYBKIE PYTANIA ───────────────────────────────────────────────────────
    st.markdown('<div style="margin-top:0.8rem"></div>', unsafe_allow_html=True)
    question_label("Przykładowe pytania")
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
                "⟳ Zamieniam pytanie na wektor · Przeszukuję bazę · Składam odpowiedź…"
                "</div>",
                unsafe_allow_html=True,
            )
            result = rag_query(question, top_k=top_k, model_name=model_name)
        sess.set_result(question, result)
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

    # Źródła
    if result["sources"]:
        render_source_chips(result["sources"], show_scores)
        for i, src in enumerate(result["sources"]):
            render_chunk_expander(src, i, show_scores)
