from __future__ import annotations

import streamlit as st

SUPPORTED_LANGUAGES = ["Auto Detect", "Python", "Java", "C++", "JavaScript", "C", "Go", "Rust"]
OUTPUT_SECTIONS = ["Explanation", "Complexity", "Line-by-Line", "Improvements", "Quiz"]


def render_sidebar() -> None:
    st.markdown(
        """
        <div class="ce-right-rail">
          <div class="ce-side-card">
            <h4>Project Information</h4>
            <div class="ce-side-list">
              <div class="ce-side-item">A public-facing code tutor UI with editorial notes and quiet chrome.</div>
              <div class="ce-side-item">Built for later backend wiring, but currently all surfaces are frontend only.</div>
            </div>
          </div>

          <div class="ce-side-card">
            <h4>Supported Languages</h4>
            <div class="ce-side-list">
        """,
        unsafe_allow_html=True,
    )
    for language in SUPPORTED_LANGUAGES:
        st.markdown(f'<div class="ce-side-item">{language}</div>', unsafe_allow_html=True)
    st.markdown(
        """
            </div>
          </div>

          <div class="ce-side-card">
            <h4>Output Sections</h4>
            <div class="ce-side-list">
        """,
        unsafe_allow_html=True,
    )
    for section in OUTPUT_SECTIONS:
        st.markdown(f'<div class="ce-side-item">{section}</div>', unsafe_allow_html=True)
    st.markdown(
        """
            </div>
          </div>

          <div class="ce-side-card">
            <h4>About Agent</h4>
            <div class="ce-side-list">
              <div class="ce-side-item">The page is organized around margin notes, not dashboard widgets.</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
