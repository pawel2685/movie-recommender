import pytest
from unittest.mock import patch

from ui.tabs.tab_main import render_tab_main


def test_render_tab_main_no_crash():
    """Smoke-test: render_tab_main should not raise when streamlit is mocked."""
    with patch("ui.tabs.tab_main.st") as mock_st:
        mock_st.text_input.return_value = ""
        mock_st.button.return_value = False
        mock_st.session_state = {}
        render_tab_main()
