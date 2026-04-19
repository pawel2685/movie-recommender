import streamlit as st


def movie_card(title: str, year: int | None, genres: list[str], score: float, description: str = ""):
    genres_html = "".join(f'<span class="genre-chip">{g}</span>' for g in genres)
    st.markdown(
        f"""
        <div class="movie-card">
            <strong>{title}</strong> {f"({year})" if year else ""}
            &nbsp;&nbsp;<em>score: {score:.2f}</em>
            <br/>{genres_html}
            <p style="margin-top:0.5rem">{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def genre_chip(label: str):
    st.markdown(f'<span class="genre-chip">{label}</span>', unsafe_allow_html=True)
