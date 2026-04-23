"""
ui/layout.py
Stałe elementy layoutu: hero header i sidebar.
"""

from __future__ import annotations
import streamlit as st

from config.settings  import DATASET_SIZE, DEFAULT_MODEL, MIN_TOP_K, MAX_TOP_K, DEFAULT_TOP_K
from ui.components    import (
    render_history_item, render_status_line,
    section_divider, section_label,
)
import utils.session as sess


# ── HERO ──────────────────────────────────────────────────────────────────────

def render_hero() -> None:
    st.markdown(f"""
    <div class="hero">
        <div class="hero-eyebrow">RAG · TMDB 5000 · Asystent AI</div>
        <h1>Asystent <em>Filmowy</em></h1>
        <p class="hero-sub">
            System odpowiadający na pytania wyłącznie na podstawie
            zamkniętej dokumentacji filmowej.
        </p>
        <div class="hero-stats">
            <div>
                <div class="hero-stat-num">{DATASET_SIZE:,}</div>
                <div class="hero-stat-label">Filmy w bazie</div>
            </div>
            <div>
                <div class="hero-stat-num">all-MiniLM</div>
                <div class="hero-stat-label">Model embeddingów</div>
            </div>
            <div>
                <div class="hero-stat-num">cos. sim.</div>
                <div class="hero-stat-label">Metryka podobieństwa</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── SIDEBAR ───────────────────────────────────────────────────────────────────

def render_sidebar() -> tuple[int, str, bool]:
    """
    Renderuje sidebar i zwraca wybrane parametry.

    Returns:
        (top_k, model_name, show_scores)
    """
    with st.sidebar:
        # Logo
        st.markdown("""
        <div class="sidebar-logo">🎬 CineRAG</div>
        <div class="sidebar-ver">v0.1 — TMDB 5000 · RAG</div>
        """, unsafe_allow_html=True)

        section_divider()

        # Status systemu
        section_label("Status systemu")
        render_status_line("Baza wektorowa: aktywna",  active=True)
        render_status_line("Model embeddingów: załadowany", active=True)
        render_status_line("LLM API: brak połączenia", active=False)

        section_divider()

        # Parametry
        section_label("Parametry")
        top_k = st.slider(
            "Liczba fragmentów (top-k)",
            MIN_TOP_K, MAX_TOP_K, DEFAULT_TOP_K,
            help="Ile najlepszych fragmentów zwrócić z bazy wektorowej",
        )
        model_name = DEFAULT_MODEL
        show_scores = st.toggle("Pokaż wyniki podobieństwa", value=True)

        section_divider()

        # Statystyki sesji
        section_label("Sesja")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Pytania", len(sess.get_history()))
        with col_b:
            st.metric("Trafienia", sess.count_hits())
        section_divider()

        # Historia
        history = sess.get_history()
        if history:
            section_label("Historia pytań")
            current_q = sess.get_current_question()
            for item in reversed(history[-8:]):
                render_history_item(item, current_q)

        section_divider()

        # Wyczyść sesję
        st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
        if st.button("🗑 Wyczyść sesję", use_container_width=True):
            sess.clear_session()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    return top_k, model_name, show_scores

def inject_sidebar_toggle() -> None:
    """
    Wstrzykuje pływający przycisk ▶ który wysuwa sidebar gdy jest schowany.
    Działa przez kliknięcie wbudowanego przycisku Streamlit via JS.
    """
    st.markdown("""
    <style>
    /* Pływający przycisk toggle */
    #sidebar-toggle-btn {
        position: fixed;
        top: 50%;
        left: 0;
        transform: translateY(-50%);
        z-index: 999999;

        width: 20px;
        height: 56px;
        background: #1a1c22;
        border: 1px solid rgba(220,160,60,0.25);
        border-left: none;
        border-radius: 0 30px 30px 0;

        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;

        color: #e0a030;
        font-size: 11px;
        transition: all 0.2s ease;
        display: none;           /* domyślnie ukryty */
        box-shadow: 4px 0 15px rgba(0,0,0,0.3);
        pointer-events: none;    /* nieaktywny gdy sidebar widoczny */
    }

    #sidebar-toggle-btn:hover {
        width: 28px;
        background: #222430;
        border-color: rgba(220,160,60,0.5);
        box-shadow: 2px 0 12px rgba(220,160,60,0.15);
    }

    /* Naprawa interakcji: pokazujemy obszar przycisku mimo ukrytego nagłówka */
    header[data-testid="stHeader"], 
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="stSidebarCollapsedControl"] * {
        visibility: visible !important;
        background: transparent !important;
    }
    </style>

    <div id="sidebar-toggle-btn" title="Otwórz menu">▶</div>

    <script>
    (function() {
        const btn = document.getElementById('sidebar-toggle-btn');
        if (!btn) return;
        
        btn.addEventListener('click', function() {
            // Szukamy przycisku wewnątrz kontrolki Streamlit
            const selectors = [
                '[data-testid="stSidebarCollapsedControl"] button',
                'button[kind="header"]',
                '.st-emotion-cache-zq5wrt button'
            ];
            
            for (const s of selectors) {
                const el = document.querySelector(s);
                if (el) {
                    el.click();
                    return;
                }
            }
        });

        // Obserwuj stan sidebara i pokazuj/ukrywaj nasz przycisk
        const observer = new MutationObserver(function() {
            const collapsed = document.querySelector('[data-testid="stSidebarCollapsedControl"]');
            btn.style.opacity       = collapsed ? '1' : '0';
            btn.style.pointerEvents = collapsed ? 'auto' : 'none';
        });

        observer.observe(document.body, { childList: true, subtree: true });
    })();
    </script>
    """, unsafe_allow_html=True)
