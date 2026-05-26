"""
ui/tabs/tab_tests.py
Zakładka "Historia" — statyczny widok historii rozmów (placeholder).
"""

from __future__ import annotations
import streamlit as st


def render() -> None:
    """Renderuje statyczny widok zakładki Historia."""

    st.markdown("""
    <div style="margin-bottom:1.0rem">
        <div class="question-label">Historia rozmów</div>
        <div style="font-size:13px;color:#444455;margin-top:4px">
            Tutaj będzie lista Twoich wcześniejszych rozmów z asystentem.
            Na razie wyświetlamy statyczny wygląd zakładki.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Przykładowe, statyczne karty rozmów
    conversations = [
        {"time": "2026-05-20 14:22", "title": "Szukaj filmów Sci-Fi", "excerpt": "Jakie filmy sci-fi polecasz z lat 80.?"},
        {"time": "2026-05-19 09:11", "title": "Polecenia dla komedii", "excerpt": "Szukam lekkich komedii romantycznych."},
        {"time": "2026-05-18 20:04", "title": "Dramaty historyczne", "excerpt": "Poleć filmy o II wojnie światowej."},
    ]

    for conv in conversations:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.04); padding:12px; border-radius:8px; margin-bottom:10px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="font-weight:600; color:#e0d8c8;">{conv['title']}</div>
                <div style="font-size:11px; color:#999999;">{conv['time']}</div>
            </div>
            <div style="font-size:13px; color:#666677; margin-top:6px">{conv['excerpt']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:1rem; font-size:12px; color:#888899">
        To tylko statyczny widok. W przyszłości załadujemy rzeczywistą historię z sesji użytkownika.
    </div>
    """, unsafe_allow_html=True)
