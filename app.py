from __future__ import annotations

import streamlit as st

from components import (
    render_editor_card,
    render_footer,
    render_hero,
    render_navbar,
    render_process_indicator,
    render_results_tabs,
    render_sidebar,
)
from styles import inject_global_styles
from core.agent import CodeExplainAgent

st.set_page_config(
    page_title="CodeExplain | Plain-English Code Tutor",
    page_icon="C",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "codeexplain_theme" not in st.session_state:
    st.session_state["codeexplain_theme"] = "Light"

inject_global_styles(st.session_state["codeexplain_theme"])

# Initialize a fresh lightweight agent on each rerun so .env changes are picked up.
st.session_state["codeexplain_agent"] = CodeExplainAgent()

# Streamlit session state defaults required by the app
if "analysis_result" not in st.session_state:
    st.session_state["analysis_result"] = None
if "code_input" not in st.session_state:
    st.session_state["code_input"] = ""
if "selected_language" not in st.session_state:
    st.session_state["selected_language"] = "python"
if "codeexplain_difficulty" not in st.session_state:
    st.session_state["codeexplain_difficulty"] = "Intermediate"
if "is_loading" not in st.session_state:
    st.session_state["is_loading"] = False

render_navbar()
render_hero()

main_col, side_col = st.columns([4.9, 1.35], gap="large", vertical_alignment="top")
with main_col:
    render_editor_card()
    render_process_indicator()
    render_results_tabs()
    render_footer()

with side_col:
    render_sidebar()
