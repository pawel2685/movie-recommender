import streamlit as st


def render_tab_about():
    st.header("O projekcie")
    st.markdown(
        """
        **CineRAG** to system rekomendacji filmów oparty na architekturze
        Retrieval-Augmented Generation (RAG).

        ### Zespół
        - **Osoba 1** – preprocessing danych (`data/`)
        - **Osoba 2** – logika RAG (`rag/`)
        - **Osoba 3** – interfejs użytkownika i testy (`ui/`, `tests/`)

        ### Technologie
        - [Streamlit](https://streamlit.io) – frontend
        - [FAISS](https://github.com/facebookresearch/faiss) / [ChromaDB](https://www.trychroma.com) – wyszukiwanie wektorowe
        - [Sentence Transformers](https://www.sbert.net) – embeddingi
        """
    )
