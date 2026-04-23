"""
ui/tabs/tab_tests.py
Zakładka "🧪 Testy" — panel testowania jakości RAG.
"""

from __future__ import annotations
import streamlit as st

from config.constants import SAMPLE_QUESTIONS, CATEGORY_COLORS, TEST_REPORT_METRICS
from ui.components import question_label
import utils.session as sess


def render() -> None:
    """Renderuje zakładkę Testy."""

    # ── NAGŁÓWEK ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom:1.2rem">
        <div class="question-label">Panel testowania jakości RAG</div>
        <div style="font-size:13px;color:#444455;margin-top:4px">
            15–20 pytań testowych w 4 kategoriach.
            Raport z trafności, halucynacji i poprawności źródeł.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KAFELKI KATEGORII ─────────────────────────────────────────────────────
    cat_cols = st.columns(len(SAMPLE_QUESTIONS))
    for col, (cat, qs) in zip(cat_cols, SAMPLE_QUESTIONS.items()):
        color = CATEGORY_COLORS[cat]
        with col:
            st.markdown(f"""
            <div style="
                background:rgba(255,255,255,0.02);
                border:1px solid {color}22;
                border-top:3px solid {color};
                border-radius:8px;
                padding:12px 14px;
                margin-bottom:12px
            ">
                <div style="font-size:13px;font-weight:600;color:{color};margin-bottom:4px">{cat}</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#333344">
                    {len(qs)} pytań
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── LISTA PYTAŃ ───────────────────────────────────────────────────────────
    selected_cat = st.selectbox(
        "Wybierz kategorię",
        list(SAMPLE_QUESTIONS.keys()),
        label_visibility="visible",
    )

    st.markdown(
        f'<div style="margin:1rem 0 0.4rem">'
        f'<div class="question-label">Pytania — {selected_cat}</div></div>',
        unsafe_allow_html=True,
    )

    for i, q in enumerate(SAMPLE_QUESTIONS[selected_cat]):
        col_q, col_run = st.columns([5, 1])
        with col_q:
            st.markdown(f"""
            <div style="
                background:#0d0f14;
                border:1px solid rgba(255,255,255,0.05);
                border-radius:6px;
                padding:9px 12px;
                font-size:13px;
                color:#666677;
                margin-bottom:6px
            ">
                <span style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#333344;margin-right:8px">
                    {i + 1:02d}
                </span>{q}
            </div>
            """, unsafe_allow_html=True)
        with col_run:
            if st.button("▶", key=f"test_{selected_cat}_{i}", help="Uruchom to pytanie"):
                sess.set_quick_question(q)
                st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── RAPORT ───────────────────────────────────────────────────────────────
    question_label("Raport z poprzednich testów")

    test_results = sess.get_test_results()
    if not test_results:
        st.markdown("""
        <div style="
            background:rgba(255,255,255,0.02);
            border:1px dashed rgba(255,255,255,0.07);
            border-radius:8px;
            padding:2rem;
            text-align:center
        ">
            <div style="font-size:28px;margin-bottom:8px">📊</div>
            <div style="font-size:13px;color:#333344">
                Brak uruchomionych testów w tej sesji.<br>
                Uruchom pytania testowe powyżej.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        cols = st.columns(len(TEST_REPORT_METRICS))
        for col, (label, val) in zip(cols, TEST_REPORT_METRICS):
            with col:
                st.metric(label, val)
