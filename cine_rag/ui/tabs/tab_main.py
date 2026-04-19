import streamlit as st

from rag.engine import rag_query
from ui.components import movie_card


def render_tab_main():
    st.header("Zapytaj o film")
    query = st.text_input("Wpisz zapytanie", placeholder="np. film sci-fi z lat 80. o podróżach w czasie")

    if st.button("Szukaj") and query:
        with st.spinner("Szukam..."):
            results = rag_query(query, top_k=st.session_state.get("top_k", 5))

        if results:
            for r in results:
                movie_card(
                    title=r.get("title", ""),
                    year=r.get("year"),
                    genres=r.get("genres", []),
                    score=r.get("score", 0.0),
                    description=r.get("description", ""),
                )
        else:
            st.info("Brak wyników dla podanego zapytania.")
