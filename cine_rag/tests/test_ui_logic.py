import pytest
from unittest.mock import patch, MagicMock


def test_render_tab_main_no_crash():
    with patch("ui.tabs.tab_main.st") as mock_st, \
         patch("ui.tabs.tab_main.sess") as mock_sess, \
         patch("ui.tabs.tab_main.rag_query", return_value={"text": None, "sources": []}):
        mock_st.text_area.return_value = ""
        mock_st.button.return_value = False
        mock_st.form.return_value.__enter__ = MagicMock(return_value=mock_st)
        mock_st.form.return_value.__exit__ = MagicMock(return_value=False)
        mock_st.form_submit_button.return_value = False
        mock_st.columns.return_value = [mock_st, mock_st, mock_st]
        mock_sess.get_current_question.return_value = ""
        mock_sess.get_current_result.return_value = None
        from ui.tabs.tab_main import render
        render(top_k=3, model_name="all-MiniLM-L6-v2", show_scores=False)
