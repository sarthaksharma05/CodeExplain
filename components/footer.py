from __future__ import annotations

import streamlit as st


def render_footer() -> None:
    st.markdown(
        """
        <div class="ce-footer">
          <div class="ce-footer-row">
            <div>
              <h4>Built with</h4>
              <div class="ce-badges" style="margin-top: 0;">
                <span class="ce-pill">Python</span>
                <span class="ce-pill">Streamlit</span>
                <span class="ce-pill">Frontend only</span>
              </div>
            </div>
            <div class="ce-footer-copy">
              Designed as a polished product shell for future AI-assisted code explanations. All visible states are UI placeholders only.
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
