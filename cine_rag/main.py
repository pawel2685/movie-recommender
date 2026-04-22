"""
main.py
Punkt startowy aplikacji CineRAG.

Uruchomienie:
    streamlit run main.py

Struktura:
    main.py                 ← jesteś tutaj
    ui/styles.py            → CSS
    ui/layout.py            → hero, sidebar
    ui/tabs/tab_main.py     → zakładka "Zapytaj"
    ui/tabs/tab_tests.py    → zakładka "Testy"
    ui/tabs/tab_about.py    → zakładka "O projekcie"
    rag/engine.py           → rag_query() (Osoba 2)
    utils/session.py        → session_state
    config/settings.py      → parametry
    config/constants.py     → stałe dane
"""
import streamlit as st


# ── KONFIGURACJA STRONY (MUSI być pierwszym wywołaniem Streamlit) ─────────────
from config.settings import PAGE_TITLE, PAGE_ICON, LAYOUT

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state="expanded",
)

# ── INICJALIZACJA SESJI ───────────────────────────────────────────────────────
from utils.session import init_session
init_session()

# ── CSS ───────────────────────────────────────────────────────────────────────
from ui.styles import inject_styles
inject_styles()

# ── LAYOUT ───────────────────────────────────────────────────────────────────
from ui.layout import render_hero, render_sidebar
render_hero()
top_k, model_name, show_scores = render_sidebar() # Tu renderujemy sidebar

# ── ZAKŁADKI ─────────────────────────────────────────────────────────────────
from ui.tabs import tab_main, tab_tests, tab_about, tab_base, tab_database

tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬  Zapytaj", "🎬  Moja Lista", "🧪  Testy", "📋  O projekcie", "⚙️  Metodologia"])

with tab1:
    tab_main.render(top_k=top_k, model_name=model_name, show_scores=show_scores)

with tab2:
    tab_database.render()

with tab3:
    tab_tests.render()

with tab4:
    tab_about.render()

with tab5:
    tab_base.render()

# ── DODATKI UI ───────────────────────────────────────────────────────────────
from ui.layout import inject_sidebar_toggle
inject_sidebar_toggle()  