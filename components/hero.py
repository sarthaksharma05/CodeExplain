from __future__ import annotations

import streamlit as st


def render_hero() -> None:
    st.markdown(
        """
        <div class="ce-hero">
          <h1 class="ce-hero-title">CodeExplain</h1>
          <div class="ce-hero-subtitle">Understand code like a developer, explained like a teacher.</div>
          <div class="ce-badges">
            <span class="ce-badge">Plain-English explanations</span>
            <span class="ce-badge">Margin-note annotations</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
