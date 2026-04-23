"""
ui/components.py
Wielokrotnie używane komponenty UI — czyste funkcje renderujące HTML.
Każda funkcja zwraca string HTML lub renderuje przez st.markdown().
"""

from __future__ import annotations
import streamlit as st
from utils.helpers import fmt_score, truncate, history_icon, history_color


# ── ANSWER CARD ───────────────────────────────────────────────────────────────

def render_answer_card(text: str, num_sources: int, model_name: str) -> None:
    st.markdown(f"""
    <div class="answer-card">
        <div class="answer-header">
            <span class="answer-badge">ODPOWIEDŹ</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#333344">
                {num_sources} fragmentów · {model_name}
            </span>
        </div>
        <div class="answer-text">{text}</div>
    </div>
    """, unsafe_allow_html=True)


def render_no_results() -> None:
    st.markdown("""
    <div class="no-results">
        <div class="no-results-icon">🔎</div>
        <div>
            <div style="font-size:13px;color:#8a4040;font-weight:600;margin-bottom:4px">
                Nie znaleziono informacji w dokumentacji
            </div>
            <div class="no-results-text">
                Baza zawiera wyłącznie informacje o filmach z datasetu TMDB 5000.
                Pytania o aktorów, reżyserów poza bazą, serwisy streamingowe
                lub inne tematy nie będą miały odpowiedzi.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── SOURCE CHIPS ──────────────────────────────────────────────────────────────

def render_source_chips(sources: list[dict], show_scores: bool) -> None:
    """Renderuje rząd chipów z nazwami plików źródłowych."""
    chips = ""
    for i, src in enumerate(sources):
        score_str = f" · {fmt_score(src['score'])}" if show_scores else ""
        chips += f"""
        <span class="source-chip">
            <span class="source-num">{i + 1}</span>
            <span class="source-name">{src['file']}{score_str}</span>
        </span>"""
    st.markdown(
        f'<div class="sources-header">Źródła</div>'
        f'<div style="margin-bottom:0.8rem">{chips}</div>',
        unsafe_allow_html=True,
    )


# ── CHUNK EXPANDER ────────────────────────────────────────────────────────────

def render_chunk_expander(src: dict, index: int, show_scores: bool) -> None:
    """Renderuje jeden rozwijany fragment dokumentu."""
    label = f"Fragment #{index + 1} — {src['file']} (chunk {src['chunk']})"
    with st.expander(label, expanded=(index == 0)):
        score_span = (
            f'<span style="margin-left:auto;font-family:JetBrains Mono,monospace;'
            f'font-size:10px;color:#c08a3a">sim: {fmt_score(src["score"])}</span>'
            if show_scores else ""
        )
        st.markdown(f"""
        <div class="chunk-card">
            <div class="chunk-meta">
                <span class="chunk-file">📄 {src['file']}</span>
                <span class="chunk-id">chunk #{src['chunk']}</span>
                {score_span}
            </div>
            <div class="chunk-text">"{src['text']}"</div>
        </div>
        """, unsafe_allow_html=True)
        if show_scores:
            st.progress(src["score"], text=None)


# ── HISTORY ITEM ──────────────────────────────────────────────────────────────

def render_history_item(item: dict, current_question: str) -> None:
    is_active = item["q"] == current_question
    color     = history_color(item.get("found", False), is_active)
    icon      = history_icon(item.get("found", False))
    label     = truncate(item["q"], 38)
    st.markdown(f"""
    <div class="history-item">
        <div class="history-q" style="color:{color}">
            <span style="opacity:0.6;font-size:10px;margin-right:4px">{icon}</span>{label}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── STATUS LINE ───────────────────────────────────────────────────────────────

def render_status_line(label: str, active: bool = True) -> None:
    if active:
        dot = '<span class="status-dot"></span>'
        color = "#333344"
    else:
        dot = '<span style="display:inline-block;width:7px;height:7px;border-radius:50%;background:#555;margin-right:6px"></span>'
        color = "#2a3a2a"
    st.markdown(
        f'<div class="status-line" style="color:{color}">{dot} {label}</div>',
        unsafe_allow_html=True,
    )


# ── SECTION DIVIDER ───────────────────────────────────────────────────────────

def section_divider() -> None:
    st.markdown(
        "<div style='margin:1.2rem 0;border-top:1px solid rgba(255,255,255,0.04)'></div>",
        unsafe_allow_html=True,
    )


def section_label(text: str) -> None:
    st.markdown(f'<div class="sidebar-label">{text}</div>', unsafe_allow_html=True)


def question_label(text: str) -> None:
    st.markdown(f'<div class="question-label">{text}</div>', unsafe_allow_html=True)
