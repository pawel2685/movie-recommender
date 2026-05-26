"""
ui/layout.py
Stałe elementy layoutu: hero header i sidebar.
"""

from __future__ import annotations
import os
import requests
from dotenv import load_dotenv
import streamlit as st

from config.settings  import DATASET_SIZE, DEFAULT_MODEL, MIN_TOP_K, MAX_TOP_K, DEFAULT_TOP_K
from ui.components    import (
    render_history_item, render_status_line,
    section_divider, section_label,
)
import utils.session as sess


T = {
    "Polski": {
        "eyebrow": "RAG · TMDB 5000 · Asystent AI",
        "title": "Asystent <em>Filmowy</em>",
        "sub": "System odpowiadający na pytania wyłącznie na podstawie zamkniętej dokumentacji filmowej.",
        "stat_movies": "Filmy w bazie",
        "stat_model": "Model embeddingów",
        "stat_metric": "Metryka podobieństwa",
        "ver": "v0.1 — TMDB 5000 · RAG",
        "status": "Status systemu",
        "status_db": "Baza wektorowa: aktywna",
        "status_model": "Model embeddingów: załadowany",
        "status_llm_on": "LLM API: aktywne",
        "status_llm_off": "LLM API: brak połączenia",
        "params": "Parametry",
        "top_k": "Liczba fragmentów (top-k)",
        "top_k_help": "Ile najlepszych fragmentów zwrócić z bazy wektorowej",
        "scores": "Pokaż wyniki podobieństwa",
        "session": "Sesja",
        "metrics_q": "Pytania",
        "metrics_h": "Trafienia",
        "history": "Historia pytań",
        "clear": "🗑 Wyczyść sesję",
        "open_menu": "Otwórz menu"
    },
    "English": {
        "eyebrow": "RAG · TMDB 5000 · AI Assistant",
        "title": "Movie <em>Assistant</em>",
        "sub": "A system that answers questions based solely on closed movie documentation.",
        "stat_movies": "Movies in database",
        "stat_model": "Embedding model",
        "stat_metric": "Similarity metric",
        "ver": "v0.1 — TMDB 5000 · RAG",
        "status": "System Status",
        "status_db": "Vector DB: active",
        "status_model": "Embedding model: loaded",
        "status_llm_on": "LLM API: active",
        "status_llm_off": "LLM API: no connection",
        "params": "Parameters",
        "top_k": "Number of chunks (top-k)",
        "top_k_help": "How many top fragments to return from the vector database",
        "scores": "Show similarity scores",
        "session": "Session",
        "metrics_q": "Questions",
        "metrics_h": "Hits",
        "history": "Question History",
        "clear": "🗑 Clear session",
        "open_menu": "Open menu"
    }
}

# ── HELPERS ──────────────────────────────────────────────────────────────────

@st.cache_data(ttl=30)
def check_ollama_status() -> bool:
    """Sprawdza dostępność serwera Ollama wysyłając lekkie zapytanie GET."""
    url = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
    try:
        resp = requests.get(f"{url}/api/tags", timeout=1)
        return resp.status_code == 200
    except:
        return False

# ── HERO ──────────────────────────────────────────────────────────────────────

def render_hero() -> None:
    lang = st.session_state.get("app_language", "Polski")
    t = T[lang]
    st.markdown(f"""
    <div class="hero">
        <div class="hero-eyebrow">{t['eyebrow']}</div>
        <h1>{t['title']}</h1>
        <p class="hero-sub">
            {t['sub']}
        </p>
        <div class="hero-stats">
            <div>
                <div class="hero-stat-num">{DATASET_SIZE:,}</div>
                <div class="hero-stat-label">{t['stat_movies']}</div>
            </div>
            <div>
                <div class="hero-stat-num">all-MiniLM</div>
                <div class="hero-stat-label">{t['stat_model']}</div>
            </div>
            <div>
                <div class="hero-stat-num">cos. sim.</div>
                <div class="hero-stat-label">{t['stat_metric']}</div>
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
    lang = st.session_state.get("app_language", "Polski")
    t = T[lang]
    with st.sidebar:
        # Logo
        st.markdown(f"""
        <div class="sidebar-logo">🎬 CineRAG</div>
        <div class="sidebar-ver">{t['ver']}</div>
        """, unsafe_allow_html=True)

        section_divider()

        llm_active = check_ollama_status()

        # Status systemu
        section_label(t['status'])
        render_status_line(t['status_db'],  active=True)
        render_status_line(t['status_model'], active=True)
        render_status_line(t['status_llm_on'] if llm_active else t['status_llm_off'], active=llm_active)

        section_divider()

        # Parametry
        section_label(t['params'])
        top_k = st.slider(
            t['top_k'],
            MIN_TOP_K, MAX_TOP_K, DEFAULT_TOP_K,
            help=t['top_k_help'],
        )
        st.selectbox(
            "Język / Language",
            options=["Polski", "English"],
            index=0,
            key="app_language"
        )
        model_name = DEFAULT_MODEL
        show_scores = st.toggle(t['scores'], value=True)

        section_divider()

        # Statystyki sesji
        section_label(t['session'])
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric(t['metrics_q'], len(sess.get_history()))
        with col_b:
            st.metric(t['metrics_h'], sess.count_hits())
        section_divider()

        # Historia
        history = sess.get_history()
        if history:
            section_label(t['history'])
            current_q = sess.get_current_question()
            for item in reversed(history[-8:]):
                render_history_item(item, current_q)

        section_divider()

        # Wyczyść sesję
        st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
        if st.button(t['clear'], use_container_width=True):
            sess.clear_session()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    return top_k, model_name, show_scores

def inject_sidebar_toggle() -> None:
    """
    Wstrzykuje pływający przycisk ▶ który wysuwa sidebar gdy jest schowany.
    Działa przez kliknięcie wbudowanego przycisku Streamlit via JS.
    """
    lang = st.session_state.get("app_language", "Polski")
    t = T[lang]
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

    <div id="sidebar-toggle-btn" title="{t['open_menu']}">▶</div>

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
