import streamlit as st

from tests.sample_questions import SAMPLE_QUESTIONS
from rag.engine import rag_query


def render_tab_tests():
    st.header("Testy systemu")
    st.write("Przetestuj system na przykładowych pytaniach.")

    for i, question in enumerate(SAMPLE_QUESTIONS):
        with st.expander(f"Pytanie {i + 1}: {question}"):
            if st.button("Uruchom", key=f"test_btn_{i}"):
                with st.spinner("Przetwarzam..."):
                    results = rag_query(question)
                st.json(results)
