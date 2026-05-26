"""
ui/tabs/tab_about.py
Zakładka "📋 O projekcie" — dokumentacja, podział pracy, stack technologiczny.
"""

import streamlit as st
from config.constants import TEAM_ROLES, TECH_STACK

T = {
    "Polski": {
        "eyebrow": "Projekt Studencki",
        "title": "Asystent RAG — Dokumentacja Filmowa",
        "desc": "System AI odpowiadający na pytania o filmach <em>wyłącznie</em> na podstawie zamkniętej bazy danych TMDB 5000. Żadna odpowiedź nie pochodzi z wiedzy modelu — tylko z zindeksowanych dokumentów.",
        "work_split": "Podział pracy",
        "tech_stack": "Stack technologiczny",
        "flow_label": "Flow aplikacji",
        "flow_steps": "Pytanie użytkownika<br><span style=\"color:#c08a3a\">→</span> Embed pytania (wektor)<br><span style=\"color:#c08a3a\">→</span> Cosine similarity search<br><span style=\"color:#c08a3a\">→</span> Top-k fragmentów<br><span style=\"color:#c08a3a\">→</span> Składanie odpowiedzi<br><span style=\"color:#c08a3a\">→</span> Wynik + źródła na ekranie",
        "footer": "CineRAG · Projekt studencki · System AI · 2026",
        "roles": {
            "🗂️": ["Osoba 1 - Paweł Magda", "Dane i przetwarzanie", "EDA · chunking · pipeline indeksowania"],
            "🧠": ["Osoba 2 - Jakub Łudzeń", "Silnik RAG", "Embeddingi · baza wektorowa · retrieval"],
            "🖥️": ["Osoba 3 - Jakub Kuszper", "Aplikacja i testy", "Interfejs · dokumentacja · raport testów"]
        },
        "groups": {
            "Dane": "Dane",
            "RAG Engine": "RAG Engine",
            "Aplikacja": "Aplikacja"
        }
    },
    "English": {
        "eyebrow": "Student Project",
        "title": "RAG Assistant — Movie Documentation",
        "desc": "AI system answering questions about movies <em>exclusively</em> based on the closed TMDB 5000 database. No answer comes from model knowledge — only from indexed documents.",
        "work_split": "Work Division",
        "tech_stack": "Tech Stack",
        "flow_label": "Application Flow",
        "flow_steps": "User question<br><span style=\"color:#c08a3a\">→</span> Question embedding (vector)<br><span style=\"color:#c08a3a\">→</span> Cosine similarity search<br><span style=\"color:#c08a3a\">→</span> Top-k chunks<br><span style=\"color:#c08a3a\">→</span> Answer synthesis<br><span style=\"color:#c08a3a\">→</span> Result + sources on screen",
        "footer": "CineRAG · Student Project · AI System · 2026",
        "roles": {
            "🗂️": ["Person 1 - Paweł Magda", "Data & Processing", "EDA · chunking · indexing pipeline"],
            "🧠": ["Person 2 - Jakub Łudzeń", "RAG Engine", "Embeddings · vector DB · retrieval"],
            "🖥️": ["Person 3 - Jakub Kuszper", "App & Testing", "Interface · documentation · test report"]
        },
        "groups": {
            "Dane": "Data",
            "RAG Engine": "RAG Engine",
            "Aplikacja": "Application"
        }
    }
}

def render() -> None:
    """Renderuje zakładkę O projekcie."""
    lang = st.session_state.get("app_language", "Polski")
    t = T[lang]

    col_info, col_tech = st.columns([3, 2])

    # ── LEWA KOLUMNA — PROJEKT I ROLE ─────────────────────────────────────────
    with col_info:
        st.markdown(f"""
        <div style="margin-bottom:1.5rem">
            <div class="question-label">{t['eyebrow']}</div>
            <div style="font-family:'DM Serif Display',serif;font-size:1.6rem;color:#e0d8c8;margin:0.3rem 0 0.6rem">
                {t['title']}
            </div>
            <div style="font-size:13px;color:#c08a3a;line-height:1.7">
                {t['desc']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f'<div class="question-label">{t["work_split"]}</div>', unsafe_allow_html=True)
        for icon, label, name, desc, color in TEAM_ROLES:
            role_t = t['roles'].get(icon, [label, name, desc])
            st.markdown(f"""
            <div style="display:flex;align-items:flex-start;gap:12px;padding:12px 0;border-bottom:1px solid rgba(255,255,255,0.04)">
                <div style="width:36px;height:36px;border-radius:8px;background:{color}22;
                            display:flex;align-items:center;justify-content:center;
                            font-size:18px;flex-shrink:0">{icon}</div>
                <div>
                    <div style="font-size:10px;letter-spacing:1px;text-transform:uppercase;
                                color:{color};font-family:'JetBrains Mono',monospace">{label}</div>
                    <div style="font-size:13px;color:#ccc0a8;font-weight:600">{role_t[1]}</div>
                    <div style="font-size:11px;color:#444455;font-family:'JetBrains Mono',monospace;margin-top:2px">{role_t[2]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── PRAWA KOLUMNA — STACK I FLOW ──────────────────────────────────────────
    with col_tech:
        st.markdown(f'<div class="question-label">{t["tech_stack"]}</div>', unsafe_allow_html=True)
        for group, items in TECH_STACK:
            tags = "".join(
                f'<span style="background:{c}15;color:{c};border:1px solid {c}33;'
                f'border-radius:5px;font-family:JetBrains Mono,monospace;'
                f'font-size:11px;padding:3px 10px">{t}</span>'
                for t, c in items
            )
            st.markdown(f"""
            <div style="margin-bottom:1rem">
                <div style="font-size:10px;letter-spacing:1.5px;text-transform:uppercase;
                            color:#333344;font-family:'JetBrains Mono',monospace;margin-bottom:6px">
                    {t['groups'].get(group, group)}
                </div>
                <div style="display:flex;flex-wrap:wrap;gap:5px">{tags}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="question-label">{t['flow_label']}</div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:11px;color:#c0c0c0;line-height:2.2">
            {t['flow_steps']}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="text-align:center;font-family:'JetBrains Mono',monospace;
                font-size:10px;color:#222233;padding:0.5rem 0">
        {t['footer']}
    </div>
    """, unsafe_allow_html=True)
