"""
ui/tabs/tab_database.py
Zakładka "🎬 Moja Lista" — zarządzanie listą filmów i wizualizacja rekomendacji.
"""

from __future__ import annotations
import streamlit as st
from ui.components import question_label


def render() -> None:
    """Renderuje zakładkę Baza Filmów."""

    # Stylizacja przycisków usuwania (Pomarańczowe tło i wyrównanie)
    st.markdown("""
        <style>
        .orange-bin button {
            background-color: #e0a030 !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            height: 80px !important; 
            width: 100% !important;
            transition: all 0.2s ease !important;
        }
        .orange-bin button:hover {
            background-color: #ffb84d !important;
            transform: scale(1.02);
        }
        </style>
    """, unsafe_allow_html=True)

    # Inicjalizacja listy w sesji, jeśli nie istnieje
    if "my_collection" not in st.session_state:
        st.session_state.my_collection = [
            {"title": "The Dark Knight", "year": "2008", "genre": "Action, Crime", "score": "9.0"},
            {"title": "Inception", "year": "2010", "genre": "Sci-Fi, Adventure", "score": "8.8"},
            {"title": "Pulp Fiction", "year": "1994", "genre": "Crime, Drama", "score": "8.9"}
        ]

    st.markdown("""
    <div style="margin-bottom:1.5rem">
        <div class="question-label">Personalizacja</div>
        <div style="font-family:'DM Serif Display',serif;font-size:1.8rem;color:#e0d8c8;margin:0.3rem 0 0.6rem">
            Twoja Baza & Rekomendacje
        </div>
        <div style="font-size:13px;color:#c08a3a;line-height:1.7">
            Zarządzaj swoją listą ulubionych tytułów i otrzymaj sugestie dopasowane do Twojego gustu
            na podstawie analizy wektorowej dokumentacji TMDB 5000.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_list, col_recs = st.columns([3, 2], gap="large")

    with col_list:
        question_label("Twoja Kolekcja")
        
        # Sekcja dodawania
        with st.container():
            new_movie_title = st.text_input(
                "Dodaj film...",
                placeholder="Wpisz tytuł filmu z bazy TMDB",
                label_visibility="collapsed",
                key="new_movie_input"
            )
            if st.button("➕ Dodaj do kolekcji", use_container_width=True):
                if new_movie_title.strip():
                    st.session_state.my_collection.append({
                        "title": new_movie_title,
                        "year": "2023",
                        "genre": "Nieznany",
                        "score": "0.0"
                    })
                    st.rerun()

        st.markdown('<div style="margin-top:1.2rem"></div>', unsafe_allow_html=True)

        # Wybór sposobu wyświetlania
        view_mode = st.radio(
            "Tryb wyświetlania",
            options=["Lista", "Kafelki", "Oś czasu"],
            horizontal=True,
            label_visibility="collapsed",
            key="view_mode_selector"
        )

        st.markdown('<div style="margin-top:1rem"></div>', unsafe_allow_html=True)

        if not st.session_state.my_collection:
            st.info("Twoja lista jest pusta. Dodaj pierwszy film powyżej!")
        
        # ── TRYB: LISTA ──────────────────────────────────────────────────────
        elif view_mode == "Lista":
            for i, movie in enumerate(st.session_state.my_collection):
                c_card, c_del = st.columns([0.88, 0.12], gap="xsmall")
                with c_card:
                    st.markdown(f"""
                    <div style="display:flex; justify-content:space-between; align-items:center; 
                                padding:12px 16px; background:rgba(255,255,255,0.02); 
                                border:1px solid rgba(220,160,60,0.1); border-radius:10px; margin-bottom:10px">
                        <div>
                            <div style="font-weight:600; color:#e0d8c8; font-size:14px">{movie['title']}</div>
                            <div style="font-size:11px; color:#666677; font-family:'JetBrains Mono',monospace; margin-top:2px">
                                {movie['year']} • {movie['genre']}
                            </div>
                        </div>
                        <div style="display:flex; align-items:center; gap:15px">
                            <span style="color:#e0a030; font-family:'JetBrains Mono',monospace; font-size:16px">★ {movie['score']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with c_del:
                    st.markdown('<div class="orange-bin">', unsafe_allow_html=True)
                    if st.button("🗑️", key=f"del_list_{i}"):
                        st.session_state.my_collection.pop(i)
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

        # ── TRYB: KAFELKI ────────────────────────────────────────────────────
        elif view_mode == "Kafelki":
            grid_cols = st.columns(2)
            for i, movie in enumerate(st.session_state.my_collection):
                with grid_cols[i % 2]:
                    with st.container(border=True):
                        st.markdown(f"""
                        <div style="height:70px">
                            <div style="font-weight:600; color:#e0d8c8; font-size:13px; margin-bottom:4px; line-height:1.2">{movie['title']}</div>
                            <div style="font-size:10px; color:#444455; font-family:'JetBrains Mono',monospace">{movie['year']} • {movie['genre']}</div>
                            <div style="margin-top:8px; color:#e0a030; font-size:11px">★ {movie['score']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        c_space, c_del_btn = st.columns([0.8, 0.2])
                        with c_del_btn:
                            # Mniejsza wysokość dla kafelków
                            st.markdown('<div class="orange-bin"><style>.orange-bin button </style>', unsafe_allow_html=True)
                            if st.button("🗑️", key=f"del_grid_{i}"):
                                st.session_state.my_collection.pop(i)
                                st.rerun()
                            st.markdown('</div>', unsafe_allow_html=True)

        # ── TRYB: OŚ CZASU ───────────────────────────────────────────────────
        elif view_mode == "Oś czasu":
            # Sortowanie po roku (malejąco)
            sorted_collection = sorted(
                st.session_state.my_collection, 
                key=lambda x: x['year'], 
                reverse=True
            )
            
            for i, movie in enumerate(sorted_collection):
                col_marker, col_content, col_action = st.columns([0.15, 0.75, 0.1])
                
                with col_marker:
                    st.markdown(f"""
                    <div style="display:flex; flex-direction:column; align-items:center;">
                        <div style="background:#e0a030; width:12px; height:12px; border-radius:50%; margin-bottom:4px; box-shadow: 0 0 8px #e0a03066"></div>
                        <div style="background:rgba(220,160,60,0.2); width:2px; height:40px;"></div>
                        <div style="font-family:'JetBrains Mono',monospace; font-size:11px; color:#c08a3a; font-weight:700; margin-top:4px">{movie['year']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_content:
                    st.markdown(f"""
                    <div style="padding-top:2px">
                        <div style="font-weight:600; color:#e0d8c8; font-size:15px">{movie['title']}</div>
                        <div style="font-size:11px; color:#555566; margin-top:2px">{movie['genre']} • ★ {movie['score']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_action:
                    st.markdown('<div class="orange-bin" style="margin-top:2px">', unsafe_allow_html=True)
                    if st.button("🗑️", key=f"del_time_{i}"):
                        # Znajdź indeks w oryginalnej liście (nieposortowanej)
                        original_idx = next(
                            idx for idx, m in enumerate(st.session_state.my_collection) 
                            if m['title'] == movie['title']
                        )
                        st.session_state.my_collection.pop(original_idx)
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('<div style="margin-bottom:12px"></div>', unsafe_allow_html=True)

    with col_recs:
        question_label("AI Sugestie")
        
        st.markdown("""
        <div style="background:linear-gradient(135deg, rgba(220,160,60,0.08) 0%, rgba(180,40,60,0.05) 100%); 
                    border:1px dashed rgba(220,160,60,0.3); padding:20px; border-radius:12px; text-align:center; margin-bottom:1.5rem">
            <div style="font-size:24px; margin-bottom:8px">✨</div>
            <div style="font-size:12px; color:#c08a3a; font-weight:500">
                Na podstawie Twojego gustu polecamy:
            </div>
        </div>
        """, unsafe_allow_html=True)

        for rec, sim in [("Memento", "94%"), ("The Prestige", "89%"), ("Joker", "82%")]:
            st.markdown(f"""
            <div style="margin-bottom:12px; padding:12px; background:#111318; 
                        border-left:3px solid #e0a030; border-radius:4px">
                <div style="font-size:13px; font-weight:600; color:#ccc0a8">{rec}</div>
                <div style="font-size:10px; color:#444455; font-family:'JetBrains Mono',monospace; margin-top:4px">
                    Zgodność profilu: {sim}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.info("💡 Silnik RAG analizuje opisy Twoich filmów i szuka w bazie TMDB dokumentów o najbardziej zbliżonych wektorach cech.")