import streamlit as st


def load_styles():
    st.markdown(
        """
        <style>
        .movie-card {
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        .genre-chip {
            display: inline-block;
            background-color: #f0f0f0;
            border-radius: 16px;
            padding: 2px 10px;
            margin: 2px;
            font-size: 0.85rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
