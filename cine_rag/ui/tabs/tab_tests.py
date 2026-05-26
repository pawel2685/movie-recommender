"""
ui/tabs/tab_tests.py
Zakładka "Historia" — historia rozmów z użytkownikiem.
"""

from __future__ import annotations
import streamlit as st

import utils.session as sess


def render() -> None:
    """Renderuje widok zakładki Historia."""

    st.markdown("""
    <div style="margin-bottom:1.0rem">
        <div class="question-label">Historia rozmów</div>
        <div style="font-size:13px;color:#444455;margin-top:4px">
            Tutaj znajduje się lista Twoich wcześniejszych rozmów z asystentem.
            Dane są przechowywane lokalnie w cookies przeglądarki.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Pobierz historię
    history_obj = sess.get_conversation_history()
    conversations = history_obj.get_history()

    if not conversations:
        st.info("📭 Brak historii rozmów. Zacznij nową rozmowę w zakładce 'Zapytaj'!")
        return

    # Przycisk do czyszczenia historii
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🗑️  Wyczyść historię", use_container_width=True):
            history_obj.clear_history()
            st.success("Historia została wyczyszczona!")
            st.rerun()

    st.markdown('<div style="margin-top:0.8rem"></div>', unsafe_allow_html=True)

    # Wyświetl rozmowy
    for idx, conv in enumerate(conversations):
        col_delete, col_content = st.columns([0.1, 0.9])

        with col_delete:
            if st.button("✕", key=f"delete_{idx}", help="Usuń ten wpis"):
                history_obj.delete_entry(idx)
                st.rerun()

        with col_content:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.04); padding:12px; border-radius:8px; margin-bottom:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div style="font-weight:600; color:#e0d8c8;">{conv['title']}</div>
                    <div style="font-size:11px; color:#999999;">{conv['time']}</div>
                </div>
                <div style="font-size:13px; color:#666677; margin-top:6px">{conv['excerpt']}</div>
            </div>
            """, unsafe_allow_html=True)

            # Ekspander do pełnej treści
            with st.expander("📖 Pokaż pełną rozmowę"):
                st.markdown("**Pytanie:**")
                st.write(conv["question"])
                st.markdown("**Odpowiedź:**")
                st.write(conv["answer"])
