from __future__ import annotations

import streamlit as st


def render_navbar() -> None:
    st.markdown(
        """
        <div class="ce-brand ce-brand--standalone">
            <div class="ce-logo" aria-hidden="true">
                <svg viewBox="0 0 48 48" role="img" aria-label="CodeExplain logo">
                    <defs>
                        <linearGradient id="ceLogoFill" x1="0" y1="0" x2="1" y2="1">
                            <stop offset="0%" stop-color="#4F7DD9" />
                            <stop offset="100%" stop-color="#3559a7" />
                        </linearGradient>
                    </defs>
                    <rect x="4" y="4" width="40" height="40" rx="13" fill="url(#ceLogoFill)" />
                    <path d="M15 18.2L10.8 24L15 29.8" stroke="white" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" fill="none" />
                    <path d="M33 18.2L37.2 24L33 29.8" stroke="white" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" fill="none" />
                    <path d="M21 31L27 17" stroke="white" stroke-width="2.4" stroke-linecap="round" />
                    <circle cx="24" cy="24" r="2.3" fill="#D49A2A" />
                </svg>
            </div>
            <div>
                <div class="ce-brand-title">CodeExplain</div>
                <div class="ce-brand-subtitle">Plain-English Code Tutor</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
