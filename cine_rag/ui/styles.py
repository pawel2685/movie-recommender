"""
ui/styles.py
Cały CSS aplikacji CineRAG w jednej funkcji inject_styles().
Wywołaj ją raz na początku main.py po set_page_config().
"""

import streamlit as st

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── RESET & BASE ── */
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #0a0b0e; }
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 0 !important;
    padding-bottom: 2rem;
    max-width: 1100px;
}

/* ── HERO ── */
.hero {
    background: linear-gradient(160deg, #111318 0%, #0d0f14 60%, #12090d 100%);
    border-bottom: 1px solid rgba(220,160,60,0.15);
    padding: 3rem 2.5rem 2.5rem;
    margin: -1rem -1rem 2rem -1rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 340px; height: 340px;
    background: radial-gradient(circle, rgba(220,160,60,0.06) 0%, transparent 70%);
    pointer-events: none;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -60px; left: 30%;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(180,40,60,0.05) 0%, transparent 70%);
    pointer-events: none;
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; letter-spacing: 3px; text-transform: uppercase;
    color: #c08a3a; margin-bottom: 0.6rem;
    display: flex; align-items: center; gap: 8px;
}
.hero-eyebrow::before {
    content: ''; display: inline-block;
    width: 20px; height: 1px; background: #c08a3a;
}
.hero h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 2.8rem; color: #f0e6d0;
    line-height: 1.1; margin: 0 0 0.5rem 0; letter-spacing: -0.5px;
}
.hero h1 em { font-style: italic; color: #e0a030; }
.hero-sub { font-size: 10px; color: #c08a3a; font-weight: 300; margin: 0; }
.hero-stats {
    display: flex; gap: 2rem;
    margin-top: 1.5rem; padding-top: 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.04);
}
.hero-stat-num {
    font-family: 'DM Serif Display', serif;
    font-size: 1.6rem; color: #e0a030; line-height: 1;
}
.hero-stat-label {
    font-size: 11px; color: #c08a3a;
    text-transform: uppercase; letter-spacing: 1px; margin-top: 2px;
}

/* ── LABELS ── */
.question-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; letter-spacing: 2px; text-transform: uppercase;
    color: #08a3a; margin-bottom: 0.4rem;
}

/* ── TEXTAREA ── */
.stTextArea textarea {
    background: #111318 !important;
    border: 1px solid rgba(220,160,60,0.2) !important;
    border-radius: 10px !important;
    color: #e0d8c8 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    padding: 14px 16px !important;
    line-height: 1.6 !important;
    transition: border-color 0.2s !important;
    resize: none !important;
}
.stTextArea textarea:focus {
    border-color: rgba(220,160,60,0.5) !important;
    box-shadow: 0 0 0 3px rgba(220,160,60,0.06) !important;
}
.stTextArea textarea::placeholder { color: #33333f !important; }

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #c08a3a 0%, #e0a030 100%) !important;
    color: #0a0b0e !important; border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important; font-size: 14px !important;
    padding: 0.55rem 1.4rem !important;
    letter-spacing: 0.3px !important; transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(220,160,60,0.3) !important;
}
.stButton > button:active { transform: translateY(0) !important; }
.btn-secondary > button {
    background: rgba(255,255,255,0.04) !important;
    color: #666677 !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
}
.btn-secondary > button:hover {
    background: rgba(255,255,255,0.07) !important;
    color: #999 !important; box-shadow: none !important;
}

/* ── ANSWER CARD ── */
.answer-card {
    background: linear-gradient(160deg, #111318 0%, #0f1015 100%);
    border: 1px solid rgba(220,160,60,0.12);
    border-radius: 14px; padding: 1.6rem 1.8rem;
    margin-top: 1.2rem; position: relative;
}
.answer-card::before {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #c08a3a, #e0a030, transparent);
    border-radius: 14px 14px 0 0;
}
.answer-header {
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 1rem; padding-bottom: 0.8rem;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.answer-badge {
    background: rgba(220,160,60,0.12); color: #c08a3a;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; letter-spacing: 2px; text-transform: uppercase;
    padding: 3px 10px; border-radius: 20px;
}
.answer-text { font-size: 15px; color: #ccc0a8; line-height: 1.75; font-weight: 300; }

/* ── SOURCES ── */
.sources-header {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; letter-spacing: 2px; text-transform: uppercase;
    color: #444455; margin: 1.4rem 0 0.6rem;
}
.source-chip {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 6px; padding: 5px 11px; margin: 3px;
    transition: all 0.15s;
}
.source-chip:hover {
    background: rgba(220,160,60,0.08);
    border-color: rgba(220,160,60,0.2);
}
.source-num {
    background: rgba(220,160,60,0.15); color: #c08a3a;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; border-radius: 3px; padding: 1px 5px;
}
.source-name { font-size: 12px; color: #666677; font-family: 'JetBrains Mono', monospace; }

/* ── CHUNK CARD ── */
.chunk-card {
    background: #0d0f14;
    border: 1px solid rgba(255,255,255,0.05);
    border-left: 3px solid #c08a3a;
    border-radius: 0 8px 8px 0; padding: 1rem 1.2rem; margin: 0.5rem 0;
}
.chunk-meta { display: flex; align-items: center; gap: 8px; margin-bottom: 0.5rem; }
.chunk-file { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #c08a3a; }
.chunk-id {
    font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #333344;
    background: rgba(255,255,255,0.03); padding: 1px 6px; border-radius: 3px;
}
.chunk-text { font-size: 13px; color: #5a5a6a; line-height: 1.6; font-style: italic; }

/* ── NO RESULTS ── */
.no-results {
    background: rgba(180,40,60,0.05);
    border: 1px solid rgba(180,40,60,0.12);
    border-radius: 10px; padding: 1.2rem 1.4rem; margin-top: 1rem;
    display: flex; align-items: flex-start; gap: 12px;
}
.no-results-icon { font-size: 20px; }
.no-results-text { font-size: 13px; color: #6a4040; line-height: 1.5; }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: #0d0f14 !important;
    border-right: 1px solid rgba(255,255,255,0.04) !important;
}
section[data-testid="stSidebar"] .block-container { padding: 1.5rem 1rem; }
.sidebar-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px; letter-spacing: 2.5px; text-transform: uppercase;
    color: #333344; margin-bottom: 0.8rem;
}
.sidebar-logo { font-family: 'DM Serif Display', serif; font-size: 1.2rem; color: #e0a030; margin-bottom: 2px; }
.sidebar-ver  { font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #222233; }

/* ── HISTORY ── */
.history-item {
    padding: 8px 10px; border-radius: 6px; cursor: pointer;
    transition: background 0.15s;
    border: 1px solid transparent; margin-bottom: 4px;
}
.history-item:hover { background: rgba(255,255,255,0.03); border-color: rgba(255,255,255,0.05); }
.history-q { font-size: 12px; color: #555566; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

/* ── STATUS DOT ── */
.status-dot {
    display: inline-block; width: 7px; height: 7px; border-radius: 50%;
    background: #22c55e; box-shadow: 0 0 6px rgba(34,197,94,0.5); margin-right: 6px;
}
.status-line { font-size: 11px; color: #333344; display: flex; align-items: center; gap: 6px; margin-bottom: 4px; }

/* ── CONTROLS ── */
.stSlider > div > div > div { background: rgba(220,160,60,0.3) !important; }
.stSlider > div > div > div > div { background: #e0a030 !important; }
.stSelectbox > div > div {
    background: #111318 !important;
    border-color: rgba(255,255,255,0.08) !important;
    color: #ccc !important;
}
.stSelectbox label, .stSlider label, .stTextArea label, .stNumberInput label {
    color: #444455 !important; font-size: 12px !important;
    font-family: 'JetBrains Mono', monospace !important;
    letter-spacing: 1px !important; text-transform: uppercase !important;
}

/* ── METRICS ── */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 8px !important; padding: 12px 14px !important;
}
[data-testid="stMetricLabel"] { color: #444455 !important; font-size: 11px !important; }
[data-testid="stMetricValue"] { color: #e0a030 !important; font-family: 'DM Serif Display', serif !important; }

/* ── EXPANDER ── */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 8px !important; color: #555566 !important;
    font-size: 12px !important; font-family: 'JetBrains Mono', monospace !important;
}
.streamlit-expanderContent {
    border: 1px solid rgba(255,255,255,0.04) !important;
    border-top: none !important; background: #0d0f14 !important;
}

/* ── TABS ── */
div[data-testid="stTabs"] button p {
    font-size: 1.15rem !important;
    font-weight: 500 !important;
}

/* ── DIVIDER ── */
hr { border: none !important; border-top: 1px solid rgba(255,255,255,0.04) !important; margin: 1.5rem 0 !important; }
</style>
"""


def inject_styles() -> None:
    """Wstrzykuje cały CSS aplikacji. Wywołaj raz w main.py."""
    st.markdown(_CSS, unsafe_allow_html=True)
