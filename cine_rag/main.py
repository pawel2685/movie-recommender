import streamlit as st

from ui.layout import render_header, render_sidebar
from ui.styles import load_styles
from ui.tabs.tab_main import render_tab_main
from ui.tabs.tab_tests import render_tab_tests
from ui.tabs.tab_about import render_tab_about
from utils.session import init_session_state

st.set_page_config(
    page_title="CineRAG",
    page_icon="🎬",
    layout="wide",
)

load_styles()
init_session_state()
render_header()
render_sidebar()

tab_main, tab_tests, tab_about = st.tabs(["Zapytaj", "Testy", "O projekcie"])

with tab_main:
    render_tab_main()

with tab_tests:
    render_tab_tests()

with tab_about:
    render_tab_about()
