"""
ui/tabs/tab_database.py
Zakładka "🎬 Moja Lista" — zarządzanie listą filmów i wizualizacja rekomendacji.
"""

from __future__ import annotations
import json
import streamlit as st
import streamlit.components.v1 as components
from ui.components import question_label
from config.settings import RAW_DIR, PROCESSED_DIR
from data.preprocessing import build_clean_dataframe

COLLECTION_PATH = PROCESSED_DIR / "my_collection.json"

@st.cache_data
def get_all_movies():
    """Wczytuje i cachuje pełną bazę filmów do wyszukiwarki."""
    return build_clean_dataframe(RAW_DIR)

def load_collection() -> list[dict]:
    """Wczytuje listę filmów z pliku JSON."""
    if COLLECTION_PATH.exists():
        try:
            with open(COLLECTION_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_collection(collection: list[dict]):
    """Zapisuje listę filmów do pliku JSON."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    with open(COLLECTION_PATH, "w", encoding="utf-8") as f:
        json.dump(collection, f, ensure_ascii=False, indent=2)


def build_user_profile(collection: list[dict], movies_df):
    """Buduje profil użytkownika na podstawie zapisanej kolekcji."""
    titles = [movie["title"] for movie in collection]
    profile_movies = movies_df[movies_df["title"].isin(titles)].copy()
    title_vote = {movie["title"]: movie.get("vote", "none") for movie in collection}

    genre_weights: dict[str, float] = {}
    cast_weights: dict[str, float] = {}
    director_weights: dict[str, float] = {}

    for _, row in profile_movies.iterrows():
        vote = title_vote.get(row["title"], "none")
        weight = 2.0 if vote == "up" else 1.0

        for genre in row["genres"]:
            genre_weights[genre] = genre_weights.get(genre, 0.0) + weight
        for actor in row["cast"]:
            cast_weights[actor] = cast_weights.get(actor, 0.0) + weight
        if row["director"]:
            director_weights[row["director"]] = director_weights.get(row["director"], 0.0) + weight

    return {
        "titles": set(titles),
        "genre_weights": genre_weights,
        "cast_weights": cast_weights,
        "director_weights": director_weights,
    }


def recommend_movies(collection: list[dict], movies_df, top_n: int = 3) -> list[dict[str, str]]:
    """Zwraca rekomendacje dla listy filmów użytkownika."""
    if not collection:
        return []

    profile_collection = [movie for movie in collection if movie.get("vote", "none") != "down"]
    if not profile_collection:
        return []

    profile = build_user_profile(profile_collection, movies_df)

    def score_row(row):
        if row["title"] in profile["titles"]:
            return -1.0

        genre_overlap = sum(profile["genre_weights"].get(genre, 0.0) for genre in row["genres"])
        cast_overlap = sum(profile["cast_weights"].get(actor, 0.0) for actor in row["cast"])
        director_match = profile["director_weights"].get(row["director"], 0.0)

        return genre_overlap * 3.0 + cast_overlap * 2.0 + director_match * 5.0 + float(row["vote_average"]) / 2.0

    candidates = movies_df[movies_df["title"].isin(profile["titles"]) == False].copy()
    candidates["score"] = candidates.apply(score_row, axis=1)
    candidates = candidates.sort_values(by=["score", "vote_average"], ascending=[False, False]).head(top_n)

    max_score = float(candidates["score"].max()) if not candidates.empty else 1.0
    if max_score <= 0:
        candidates = movies_df[movies_df["title"].isin(profile["titles"]) == False].sort_values(
            by="vote_average", ascending=False
        ).head(top_n)
        max_score = float(candidates["vote_average"].max() or 1.0)

    recommendations = []
    for _, row in candidates.iterrows():
        normalized = int(min(100, max(0, row["score"] / max_score * 100))) if max_score else 0
        recommendations.append({
            "title": row["title"],
            "year": str(int(row["release_year"])),
            "genre": ", ".join(row["genres"] if row["genres"] else []),
            "match": f"{normalized}%"
        })

    return recommendations


# ---------------------------------------------------------------------------
# Pomocnik: wstrzykuje JS kolorujący przyciski głosowania po każdym rerunie
# ---------------------------------------------------------------------------
def _inject_vote_button_styles(collection: list[dict]) -> None:
    """
    Streamlit/React przerenderowuje DOM po każdym kliknięciu i nadpisuje
    inline style ustawione przez setTimeout. Rozwiązanie: MutationObserver
    obserwuje drzewo DOM rodzica i natychmiast przywraca style za każdym
    razem gdy React coś zmieni. childList+subtree łapie dodawanie/usuwanie
    węzłów (czyli re-rendery Reacta), ale NIE łapie zmian atrybutów style
    (czyli naszych własnych applyStyle) — nie ma więc pętli nieskończonej.
    """
    vote_states    = [m.get("vote", "none") for m in collection]
    vote_states_js = json.dumps(vote_states)
    up_emoji   = "\U0001F44D"   # 👍
    down_emoji = "\U0001F44E"   # 👎

    js_code = f"""
    <script>
    (function() {{
        var STATES     = {vote_states_js};
        var UP_EMOJI   = '{up_emoji}';
        var DOWN_EMOJI = '{down_emoji}';

        /* ── Kolory ─────────────────────────────────────────────────────────
           DEFAULT     — ciemne tło zamiast pomarańczowego motywu Streamlita
           UP_ACTIVE   — zielone po kliknięciu 👍
           DOWN_ACTIVE — czerwone po kliknięciu 👎                           */
        var DEFAULT     = {{ bg: '#1c2030', color: '#c8c8c8', shadow: 'inset 0 0 0 1px #3a3f55' }};
        var UP_ACTIVE   = {{ bg: '#1a3d1a', color: '#7dff7d', shadow: 'inset 0 0 0 3px #3a8a3a' }};
        var DOWN_ACTIVE = {{ bg: '#4a1a1a', color: '#ff7d7d', shadow: 'inset 0 0 0 3px #c83a3a' }};

        function applyStyle(btn, style) {{
            btn.style.setProperty('background-color', style.bg,     'important');
            btn.style.setProperty('color',            style.color,  'important');
            btn.style.setProperty('box-shadow',       style.shadow, 'important');
        }}

        function run() {{
            var doc      = window.parent.document;
            var allBtns  = Array.from(doc.querySelectorAll('button'));
            var voteBtns = allBtns.filter(function(b) {{
                var t = b.textContent.trim();
                return t === UP_EMOJI || t === DOWN_EMOJI;
            }});

            /* Kolejność w DOM: up_0, down_0, up_1, down_1, ... */
            for (var i = 0; i < STATES.length; i++) {{
                var upBtn   = voteBtns[i * 2];
                var downBtn = voteBtns[i * 2 + 1];
                if (!upBtn || !downBtn) continue;
                applyStyle(upBtn,   STATES[i] === 'up'   ? UP_ACTIVE   : DEFAULT);
                applyStyle(downBtn, STATES[i] === 'down' ? DOWN_ACTIVE : DEFAULT);
            }}
        }}

        /* ── MutationObserver ───────────────────────────────────────────────
           Uruchamia run() za każdym razem gdy React doda/usunie węzeł DOM.
           childList+subtree NIE reaguje na zmiany atrybutu "style",
           więc applyStyle() wewnątrz run() nie wywoła pętli nieskończonej. */
        function startObserver() {{
            var observer = new MutationObserver(function() {{
                clearTimeout(window._voteTimer);
                window._voteTimer = setTimeout(run, 40);
            }});
            observer.observe(window.parent.document.body, {{
                childList: true,
                subtree:   true
            }});
        }}

        /* Pierwsze uruchomienie po wyrenderowaniu, potem włącz obserwator */
        setTimeout(run, 150);
        setTimeout(startObserver, 300);
    }})();
    </script>
    """
    components.html(js_code, height=0)


def render() -> None:
    """Renderuje zakładkę Baza Filmów."""

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
        /* Bazowy styl przycisków głosowania — JS nadpisuje aktywne */
        div[data-testid="stButton"] button {
            transition: background-color 0.15s ease, color 0.15s ease, box-shadow 0.15s ease !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            line-height: 1 !important;
            padding: 0.35rem 0.7rem !important;
        }
        /* Większe przyciski + w rekomendacjach */
        div[data-testid="stButton"] button[title="Dodaj film do listy"] {
            min-width: 48px !important;
            min-height: 48px !important;
            font-size: 24px !important;
            padding: 0.3rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

    if "my_collection" not in st.session_state:
        st.session_state.my_collection = load_collection()

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

        with st.container():
            all_movies_df = get_all_movies()
            movie_titles = sorted(all_movies_df["title"].unique().tolist())

            selected_title = st.selectbox(
                "Wyszukaj film w bazie TMDB...",
                options=[""] + movie_titles,
                format_func=lambda x: "🔍 Zacznij wpisywać tytuł filmu..." if x == "" else x,
                label_visibility="collapsed"
            )

            if st.button("➕ Dodaj do kolekcji", use_container_width=True):
                if selected_title:
                    if any(m['title'] == selected_title for m in st.session_state.my_collection):
                        st.toast(f"Film '{selected_title}' jest już na Twojej liście!", icon="ℹ️")
                    else:
                        movie_data = all_movies_df[all_movies_df["title"] == selected_title].iloc[0]
                        st.session_state.my_collection.append({
                            "title": str(movie_data["title"]),
                            "year": str(movie_data["release_year"]),
                            "genre": ", ".join(movie_data["genres"]),
                            "score": str(movie_data["vote_average"]),
                            "vote": "none"
                        })
                        save_collection(st.session_state.my_collection)
                        st.rerun()

        st.markdown('<div style="margin-top:1.2rem"></div>', unsafe_allow_html=True)

        st.markdown('<div style="font-size:12px; color:#c8c8c8; margin-bottom:0.3rem; letter-spacing:0.04em">Widok</div>', unsafe_allow_html=True)
        view_mode = st.radio(
            "Tryb wyświetlania",
            options=["Lista", "Kafelki", "Oś czasu"],
            horizontal=True,
            label_visibility="collapsed",
            key="view_mode_selector"
        )

        st.markdown('<div style="margin-top:1rem"></div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:12px; color:#c8c8c8; margin-bottom:0.3rem; letter-spacing:0.04em">Sortuj</div>', unsafe_allow_html=True)
        sort_option = st.radio(
            "Sortuj listę filmów",
            options=["Domyślnie", "Alfabetycznie", "Ocena (malejąco)", "Rok (malejąco)"],
            horizontal=True,
            label_visibility="collapsed",
            key="collection_sort_option"
        )

        if sort_option == "Alfabetycznie":
            collection_display = sorted(st.session_state.my_collection, key=lambda x: x["title"])
        elif sort_option == "Ocena (malejąco)":
            collection_display = sorted(
                st.session_state.my_collection,
                key=lambda x: float(x.get("score") or 0.0),
                reverse=True
            )
        elif sort_option == "Rok (malejąco)":
            collection_display = sorted(
                st.session_state.my_collection,
                key=lambda x: int(x.get("year") or 0),
                reverse=True
            )
        else:
            collection_display = list(st.session_state.my_collection)

        if not st.session_state.my_collection:
            st.info("Twoja lista jest pusta. Dodaj pierwszy film powyżej!")

        # ── TRYB: LISTA ──────────────────────────────────────────────────────
        elif view_mode == "Lista":
            for movie in collection_display:
                vote_status = movie.get("vote", "none")
                original_idx = next(
                    (idx for idx, m in enumerate(st.session_state.my_collection) if m["title"] == movie["title"]),
                    None
                )

                c_card, c_del = st.columns([0.78, 0.22], gap="xsmall")
                with c_card:
                    vote_label = {"up": "Ocena: 👍", "down": "Ocena: 👎"}.get(vote_status, "Brak oceny")

                    st.markdown(f"""
                    <div style="display:flex; justify-content:space-between; align-items:center;
                                padding:12px 16px; background:rgba(255,255,255,0.02);
                                border:1px solid rgba(220,160,60,0.1); border-radius:10px; margin-bottom:6px">
                        <div>
                            <div style="font-weight:600; color:#e0d8c8; font-size:14px">{movie['title']}</div>
                            <div style="font-size:11px; color:#666677; font-family:'JetBrains Mono',monospace; margin-top:2px">
                                {movie['year']} • {movie['genre']}
                            </div>
                        </div>
                        <div style="text-align:right">
                            <div style="color:#e0a030; font-family:'JetBrains Mono',monospace; font-size:16px">★ {movie['score']}</div>
                            <div style="font-size:10px; color:#999999; margin-top:4px">{vote_label}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    vote_col_up, vote_col_down = st.columns([0.5, 0.5], gap="small")
                    with vote_col_up:
                        if st.button("👍", key=f"vote_up_{movie['title']}", use_container_width=True):
                            if original_idx is not None:
                                new_vote = "none" if vote_status == "up" else "up"
                                st.session_state.my_collection[original_idx]["vote"] = new_vote
                                save_collection(st.session_state.my_collection)
                                st.rerun()
                    with vote_col_down:
                        if st.button("👎", key=f"vote_down_{movie['title']}", use_container_width=True):
                            if original_idx is not None:
                                new_vote = "none" if vote_status == "down" else "down"
                                st.session_state.my_collection[original_idx]["vote"] = new_vote
                                save_collection(st.session_state.my_collection)
                                st.rerun()

                with c_del:
                    st.markdown('<div class="orange-bin">', unsafe_allow_html=True)
                    if st.button("🗑️", key=f"del_list_{movie['title']}"):
                        if original_idx is not None:
                            st.session_state.my_collection.pop(original_idx)
                            save_collection(st.session_state.my_collection)
                            st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

            if st.session_state.my_collection:
                _inject_vote_button_styles(st.session_state.my_collection)

        # ── TRYB: KAFELKI ────────────────────────────────────────────────────
        elif view_mode == "Kafelki":
            grid_cols = st.columns(2)
            for idx, movie in enumerate(collection_display):
                vote_status = movie.get("vote", "none")
                original_idx = next(
                    (i for i, m in enumerate(st.session_state.my_collection) if m["title"] == movie["title"]),
                    None
                )
                with grid_cols[idx % 2]:
                    with st.container(border=True):
                        st.markdown(f"""
                        <div style="height:52px; padding:6px 4px;">
                            <div style="font-weight:600; color:#e0d8c8; font-size:13px; margin-bottom:2px; line-height:1.1">{movie['title']}</div>
                            <div style="font-size:10px; color:#444455; font-family:'JetBrains Mono',monospace">{movie['year']} • {movie['genre']} • <span style='color:#e0a030'>★ {movie['score']}</span></div>
                        </div>
                        """, unsafe_allow_html=True)

                        vote_label = {"up": "Ocena: 👍", "down": "Ocena: 👎"}.get(vote_status, "")
                        if vote_label:
                            st.markdown(f"<div style='font-size:11px; color:#999999; margin-bottom:4px'>{vote_label}</div>", unsafe_allow_html=True)

                        # Mniejsze odstępy między przyciskami — bardziej zwarte ustawienie
                        vote_cols = st.columns([0.45, 0.45], gap="small")
                        with vote_cols[0]:
                            if st.button("👍", key=f"vote_up_grid_{movie['title']}", use_container_width=True):
                                if original_idx is not None:
                                    new_vote = "none" if vote_status == "up" else "up"
                                    st.session_state.my_collection[original_idx]["vote"] = new_vote
                                    save_collection(st.session_state.my_collection)
                                    st.rerun()
                        with vote_cols[1]:
                            if st.button("👎", key=f"vote_down_grid_{movie['title']}", use_container_width=True):
                                if original_idx is not None:
                                    new_vote = "none" if vote_status == "down" else "down"
                                    st.session_state.my_collection[original_idx]["vote"] = new_vote
                                    save_collection(st.session_state.my_collection)
                                    st.rerun()

                        # Szerszy przycisk kosza i wyśrodkowanie ikony
                        # Mniejszy, wyśrodkowany przycisk kosza — redukujemy odstęp
                        c_del_btn = st.columns([0.28, 0.72])[0]
                        with c_del_btn:
                            st.markdown(
                                '<div class="orange-bin" style="display:flex; align-items:center; justify-content:center; height:44px; width:100%; padding:0;">',
                                unsafe_allow_html=True,
                            )
                            if st.button("🗑️", key=f"del_grid_{movie['title']}", use_container_width=True):
                                if original_idx is not None:
                                    st.session_state.my_collection.pop(original_idx)
                                    save_collection(st.session_state.my_collection)
                                    st.rerun()
                            st.markdown('</div>', unsafe_allow_html=True)

        # ── TRYB: OŚ CZASU ───────────────────────────────────────────────────
        elif view_mode == "Oś czasu":
            sorted_collection = sorted(
                st.session_state.my_collection,
                key=lambda x: x['year'],
                reverse=True
            )

            for i, movie in enumerate(sorted_collection):
                original_idx = next(
                    (idx for idx, m in enumerate(st.session_state.my_collection) if m['title'] == movie['title']),
                    None
                )
                vote_status = movie.get("vote", "none")

                col_marker, col_content, col_action = st.columns([0.10, 0.65, 0.25])

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
                    # Szersze przyciski oceny — kolumna akcji ma teraz większy udział
                    vote_cols = st.columns([1, 1], gap="small")
                    with vote_cols[0]:
                        if st.button("👍", key=f"vote_up_time_{movie['title']}", use_container_width=True):
                            if original_idx is not None:
                                new_vote = "none" if vote_status == "up" else "up"
                                st.session_state.my_collection[original_idx]["vote"] = new_vote
                                save_collection(st.session_state.my_collection)
                                st.rerun()
                    with vote_cols[1]:
                        if st.button("👎", key=f"vote_down_time_{movie['title']}", use_container_width=True):
                            if original_idx is not None:
                                new_vote = "none" if vote_status == "down" else "down"
                                st.session_state.my_collection[original_idx]["vote"] = new_vote
                                save_collection(st.session_state.my_collection)
                                st.rerun()

                    st.markdown('<div class="orange-bin" style="margin-top:0.4rem">', unsafe_allow_html=True)
                    if st.button("🗑️", key=f"del_time_{movie['title']}"):
                        if original_idx is not None:
                            st.session_state.my_collection.pop(original_idx)
                            save_collection(st.session_state.my_collection)
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

        recommendations = recommend_movies(st.session_state.my_collection, all_movies_df)

        if not recommendations:
            st.info("Dodaj filmy do swojej listy, aby otrzymać rekomendacje AI automatycznie.")
        else:
            for movie in recommendations:
                row_cols = st.columns([0.8, 0.2], gap='small')
                with row_cols[0]:
                    st.markdown(f"""
                    <div style="margin-bottom:14px; padding:14px; background:#111318;
                                border-left:3px solid #e0a030; border-radius:8px">
                        <div style="font-size:14px; font-weight:700; color:#e0d8c8">{movie['title']} ({movie['year']})</div>
                        <div style="font-size:11px; color:#888899; margin-top:4px">{movie['genre']}</div>
                        <div style="font-size:10px; color:#c08a3a; font-family:'JetBrains Mono',monospace; margin-top:8px">
                            Zgodność profilu: {movie['match']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with row_cols[1]:
                    if st.button('➕', key=f"add_rec_{movie['title']}", help='Dodaj film do listy', use_container_width=True):
                        if any(m['title'] == movie['title'] for m in st.session_state.my_collection):
                            st.toast(f"Film '{movie['title']}' jest już na Twojej liście!", icon='ℹ️')
                        else:
                            movie_data = all_movies_df[all_movies_df['title'] == movie['title']].iloc[0]
                            st.session_state.my_collection.append({
                                'title': str(movie_data['title']),
                                'year': str(movie_data['release_year']),
                                'genre': ', '.join(movie_data['genres']),
                                'score': str(movie_data['vote_average']),
                                'vote': 'none'
                            })
                            save_collection(st.session_state.my_collection)
                            st.toast(f"Dodano '{movie['title']}' do Twojej listy!", icon='✅')
                            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.info("💡 Silnik RAG analizuje opisy Twoich filmów i szuka w bazie TMDB dokumentów o najbardziej zbliżonych wektorach cech.")