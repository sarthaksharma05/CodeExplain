from __future__ import annotations

import streamlit as st

THEME_TOKENS = {
    "Light": {
        "bg": "#E7EBF1",
        "surface": "#F4F7FB",
        "surface_alt": "#EAEFF5",
        "panel": "#DDE4ED",
        "panel_2": "#F8FAFC",
        "border": "#CBD4E1",
        "text": "#132238",
        "muted": "#5F6C83",
        "accent": "#4F7DD9",
        "accent_soft": "rgba(79, 125, 217, 0.12)",
        "note": "#D49A2A",
        "success": "#2F8F6B",
        "shadow": "0 16px 36px rgba(19, 34, 56, 0.08)",
    },
    "Dark": {
        "bg": "#0D1521",
        "surface": "#121C2B",
        "surface_alt": "#162233",
        "panel": "#1A273A",
        "panel_2": "#0F1724",
        "border": "#26364D",
        "text": "#EAF0F8",
        "muted": "#8A97AA",
        "accent": "#6D8FE3",
        "accent_soft": "rgba(109, 143, 227, 0.16)",
        "note": "#D4A44C",
        "success": "#4BAA84",
        "shadow": "0 18px 42px rgba(0, 0, 0, 0.34)",
    },
}


def inject_global_styles(theme: str) -> None:
    tokens = THEME_TOKENS.get(theme, THEME_TOKENS["Light"])
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600;6..72,700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

        :root {{
            --ce-bg: {tokens['bg']};
            --ce-surface: {tokens['surface']};
            --ce-surface-alt: {tokens['surface_alt']};
            --ce-panel: {tokens['panel']};
            --ce-panel-2: {tokens['panel_2']};
            --ce-border: {tokens['border']};
            --ce-text: {tokens['text']};
            --ce-muted: {tokens['muted']};
            --ce-accent: {tokens['accent']};
            --ce-accent-soft: {tokens['accent_soft']};
            --ce-note: {tokens['note']};
            --ce-success: {tokens['success']};
            --ce-shadow: {tokens['shadow']};
            --ce-warning: #D49A2A;
            --ce-radius: 14px;
            --ce-radius-sm: 12px;
            --ce-radius-xs: 10px;
        }}

        html, body, [data-testid="stAppViewContainer"] {{
            background: var(--ce-bg) !important;
            color: var(--ce-text) !important;
        }}

        html, body, [data-testid="stAppViewContainer"], .stApp {{
            font-family: 'Inter', sans-serif;
        }}

        [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu, footer {{
            visibility: hidden;
            height: 0;
        }}

        .block-container {{
            padding-top: 1.1rem;
            padding-bottom: 2rem;
            max-width: 1500px;
        }}

        [data-testid="column"] {{
            min-width: 0;
        }}

        .ce-topbar, .ce-hero, .ce-card, .ce-side-card, .ce-progress-card, .ce-footer {{
            background: var(--ce-surface);
            border: 1px solid var(--ce-border);
            border-radius: var(--ce-radius);
            box-shadow: var(--ce-shadow);
        }}

        .ce-topbar {{
            padding: 0.9rem 1rem;
            margin-bottom: 1rem;
            background: linear-gradient(180deg, var(--ce-surface) 0%, var(--ce-panel-2) 100%);
        }}

        .ce-topbar-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            flex-wrap: wrap;
        }}

        .ce-topbar-row--brand-only {{
            justify-content: flex-start;
        }}

        .ce-brand {{
            display: flex;
            align-items: center;
            gap: 1.1rem;
            min-width: 220px;
        }}

        .ce-logo {{
            width: 42px;
            height: 42px;
            border-radius: 12px;
            background: transparent;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            box-shadow: 0 10px 18px rgba(79, 125, 217, 0.16);
        }}

        .ce-brand-title {{
            font-size: 1rem;
            font-weight: 650;
            line-height: 1.1;
            color: var(--ce-text);
        }}

        .ce-brand-subtitle {{
            font-size: 0.82rem;
            color: var(--ce-muted);
            margin-top: 0.1rem;
        }}

        .ce-top-actions {{
            display: flex;
            align-items: center;
            gap: 0.55rem;
            flex-wrap: wrap;
            justify-content: flex-end;
        }}

        .ce-hero {{
            padding: 2rem 1.6rem;
            margin-bottom: 1.1rem;
            background: linear-gradient(180deg, var(--ce-surface) 0%, var(--ce-panel-2) 100%);
        }}

        .ce-hero-title {{
            font-size: clamp(2.2rem, 4vw, 4.15rem);
            line-height: 1.02;
            letter-spacing: -0.06em;
            margin: 0;
            color: var(--ce-text);
            font-weight: 650;
            font-family: 'Newsreader', serif;
        }}

        .ce-hero-subtitle {{
            margin-top: 0.65rem;
            color: var(--ce-muted);
            font-size: 1.05rem;
            line-height: 1.6;
            max-width: 720px;
        }}

        .ce-badges {{
            display: flex;
            gap: 0.6rem;
            flex-wrap: wrap;
            margin-top: 1.1rem;
        }}

        .ce-badge {{
            display: inline-flex;
            align-items: center;
            padding: 0.52rem 0.8rem;
            border-radius: 12px;
            background: var(--ce-panel-2);
            border: 1px solid var(--ce-border);
            color: var(--ce-text);
            font-size: 0.9rem;
            font-weight: 550;
        }}

        .ce-layout {{
            margin-top: 0.25rem;
        }}

        .ce-card, .ce-side-card, .ce-progress-card, .ce-footer {{
            padding: 1rem;
        }}

        .ce-card {{
            margin-bottom: 1rem;
            background: linear-gradient(180deg, var(--ce-surface) 0%, var(--ce-panel-2) 100%);
        }}

        .ce-card-title {{
            font-size: 0.96rem;
            font-weight: 700;
            color: var(--ce-text);
            margin-bottom: 0.25rem;
        }}

        .ce-card-subtitle {{
            color: var(--ce-muted);
            font-size: 0.86rem;
            line-height: 1.5;
            margin-bottom: 1rem;
        }}

        .ce-label {{
            display: block;
            font-size: 0.82rem;
            color: var(--ce-muted);
            margin-bottom: 0.35rem;
            font-weight: 550;
            letter-spacing: 0.01em;
        }}

        .ce-inline-note {{
            color: var(--ce-muted);
            font-size: 0.82rem;
        }}

        .ce-button-row {{
            display: flex;
            gap: 0.55rem;
            flex-wrap: wrap;
            margin-top: 1rem;
        }}

        .ce-progress-card {{
            margin-top: 0.9rem;
            background: linear-gradient(180deg, var(--ce-surface) 0%, var(--ce-panel-2) 100%);
        }}

        .ce-progress-list {{
            display: grid;
            gap: 0.6rem;
            margin-top: 0.9rem;
        }}

        .ce-progress-item {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.8rem 0.9rem;
            border-radius: var(--ce-radius-sm);
            border: 1px solid var(--ce-border);
            background: var(--ce-panel-2);
        }}

        .ce-progress-dot {{
            width: 0.7rem;
            height: 0.7rem;
            border-radius: 999px;
            background: var(--ce-note);
            box-shadow: 0 0 0 5px rgba(212, 154, 42, 0.12);
            flex: 0 0 auto;
        }}

        .ce-progress-step {{
            color: var(--ce-text);
            font-size: 0.92rem;
            font-weight: 550;
        }}

        .ce-progress-status {{
            color: var(--ce-muted);
            font-size: 0.82rem;
            margin-left: auto;
        }}

        .ce-right-rail {{
            position: sticky;
            top: 1rem;
            display: grid;
            gap: 0.85rem;
        }}

        .ce-side-card h4, .ce-footer h4 {{
            margin: 0 0 0.75rem 0;
            font-size: 0.92rem;
            color: var(--ce-text);
        }}

        .ce-side-list {{
            display: grid;
            gap: 0.5rem;
        }}

        .ce-side-item {{
            padding: 0.7rem 0.8rem;
            border: 1px solid var(--ce-border);
            border-radius: var(--ce-radius-sm);
            background: var(--ce-panel-2);
            color: var(--ce-text);
            font-size: 0.88rem;
        }}

        .ce-pill {{
            display: inline-flex;
            align-items: center;
            padding: 0.38rem 0.62rem;
            border: 1px solid var(--ce-border);
            border-radius: 12px;
            background: var(--ce-panel-2);
            color: var(--ce-text);
            font-size: 0.8rem;
            font-weight: 550;
        }}

        .ce-section {{
            margin-top: 0.9rem;
        }}

        .ce-placeholder-box {{
            border: 1px dashed var(--ce-border);
            border-radius: var(--ce-radius-sm);
            background: var(--ce-panel-2);
            color: var(--ce-muted);
            padding: 1rem;
        }}

        .ce-placeholder-row {{
            display: flex;
            align-items: center;
            gap: 0.9rem;
            padding: 0.85rem 0.95rem;
            border-radius: 12px;
            border: 1px solid var(--ce-border);
            background: var(--ce-panel-2);
            position: relative;
        }}

        .ce-placeholder-row::before {{
            content: '';
            position: absolute;
            left: 0.9rem;
            top: 50%;
            width: 0.65rem;
            height: 1px;
            background: var(--ce-note);
            opacity: 0.55;
        }}

        .ce-row-index {{
            width: 2rem;
            height: 2rem;
            border-radius: 10px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: rgba(212, 154, 42, 0.12);
            color: var(--ce-note);
            font-size: 0.82rem;
            font-weight: 700;
            flex: 0 0 auto;
            margin-left: 0.55rem;
        }}

        .ce-placeholder-line {{
            height: 0.72rem;
            border-radius: 999px;
            background: linear-gradient(90deg, rgba(95, 108, 131, 0.16), rgba(95, 108, 131, 0.28));
            width: 100%;
        }}

        .ce-checklist {{
            display: grid;
            gap: 0.65rem;
        }}

        .ce-check-item {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.78rem 0.9rem;
            border: 1px solid var(--ce-border);
            border-radius: var(--ce-radius-sm);
            background: var(--ce-panel-2);
            color: var(--ce-text);
        }}

        .ce-checkbox {{
            width: 1rem;
            height: 1rem;
            border-radius: 4px;
            border: 1.5px solid var(--ce-border);
            background: var(--ce-panel-2);
            flex: 0 0 auto;
        }}

        .ce-quiz-grid {{
            display: grid;
            gap: 0.9rem;
        }}

        .ce-quiz-card {{
            padding: 0.95rem;
            border: 1px solid var(--ce-border);
            border-radius: var(--ce-radius-sm);
            background: linear-gradient(180deg, var(--ce-surface) 0%, var(--ce-panel-2) 100%);
            position: relative;
            overflow: hidden;
        }}

        .ce-quiz-card::after {{
            content: 'Margin note';
            position: absolute;
            top: 0.85rem;
            right: 0.9rem;
            font-size: 0.72rem;
            color: var(--ce-note);
            letter-spacing: 0.03em;
            text-transform: uppercase;
        }}

        .ce-quiz-question {{
            font-weight: 650;
            margin-bottom: 0.75rem;
            color: var(--ce-text);
        }}

        .ce-quiz-options {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.55rem;
            margin-bottom: 0.8rem;
        }}

        .ce-quiz-option {{
            border: 1px solid var(--ce-border);
            border-radius: 12px;
            background: var(--ce-panel-2);
            color: var(--ce-text);
            padding: 0.65rem 0.75rem;
            text-align: left;
            font-size: 0.9rem;
        }}

        .ce-note-rail {{
            border-left: 1px solid var(--ce-border);
            padding-left: 1rem;
            display: grid;
            gap: 0.65rem;
        }}

        .ce-note-card {{
            position: relative;
            padding: 0.85rem 0.9rem 0.85rem 1rem;
            border: 1px solid var(--ce-border);
            border-radius: 12px;
            background: var(--ce-panel-2);
        }}

        .ce-note-card::before {{
            content: '';
            position: absolute;
            left: -1.05rem;
            top: 1.05rem;
            width: 0.8rem;
            height: 1px;
            background: var(--ce-note);
        }}

        .ce-note-kicker {{
            color: var(--ce-note);
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 0.35rem;
            font-weight: 700;
        }}

        .ce-code-label {{
            color: var(--ce-muted);
            font-size: 0.8rem;
            letter-spacing: 0.02em;
            margin-bottom: 0.4rem;
            text-transform: uppercase;
        }}

        .ce-editor-shell {{
            border: 1px solid var(--ce-border);
            border-radius: var(--ce-radius);
            background: linear-gradient(180deg, var(--ce-panel) 0%, var(--ce-panel-2) 100%);
            padding: 1rem;
        }}

        .ce-inline-pills {{
            display: flex;
            gap: 0.55rem;
            flex-wrap: wrap;
            margin-top: 0.75rem;
        }}

        .ce-chip {{
            border: 1px solid var(--ce-border);
            border-radius: 12px;
            background: var(--ce-panel-2);
            color: var(--ce-text);
            padding: 0.42rem 0.7rem;
            font-size: 0.82rem;
            font-weight: 600;
        }}

        .ce-tab-shell .stTabs [data-baseweb="tab-list"] {{
            gap: 0.45rem;
            flex-wrap: wrap;
            border-bottom: 1px solid var(--ce-border);
        }}

        .ce-tab-shell .stTabs [data-baseweb="tab"] {{
            background: var(--ce-panel-2);
            border-radius: 12px;
            border: 1px solid var(--ce-border);
            height: 2.55rem;
            padding: 0 0.9rem;
        }}

        .ce-tab-shell .stTabs [aria-selected="true"] {{
            background: var(--ce-accent-soft);
            border-color: rgba(79, 140, 255, 0.3);
        }}

        .ce-tab-shell [data-testid="stHorizontalBlock"] {{
            gap: 0.8rem;
        }}

        .stSelectbox [data-baseweb="select"], .stTextArea textarea, .stRadio [role="radiogroup"] {{
            border-radius: 12px;
        }}

        .stSelectbox div[data-baseweb="select"] > div, .stTextArea textarea {{
            background: var(--ce-panel-2) !important;
            border-color: var(--ce-border) !important;
            color: var(--ce-text) !important;
        }}

        .stRadio label {{
            background: var(--ce-panel-2);
            border: 1px solid var(--ce-border);
            border-radius: 12px;
            padding: 0.3rem 0.55rem;
        }}

        .stTextArea textarea {{
            min-height: 350px;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.94rem;
        }}

        .stButton > button {{
            border-radius: 12px;
            transition: transform 140ms ease, box-shadow 140ms ease, border-color 140ms ease, background 140ms ease;
        }}

        .stButton > button:hover {{
            transform: translateY(-1px);
        }}

        .stButton > button[kind="primary"] {{
            background: var(--ce-accent);
            color: white;
            border: 1px solid var(--ce-accent);
        }}

        .stButton > button[kind="primary"]:hover {{
            box-shadow: 0 14px 24px rgba(79, 140, 255, 0.24);
        }}

        .ce-footer {{
            margin-top: 1rem;
            background: linear-gradient(180deg, var(--ce-surface) 0%, var(--ce-panel-2) 100%);
        }}

        .ce-footer-row {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 1rem;
            flex-wrap: wrap;
        }}

        .ce-footer-copy {{
            color: var(--ce-muted);
            font-size: 0.88rem;
            line-height: 1.55;
            max-width: 620px;
        }}

        .ce-right-rail .ce-side-card:first-child {{
            border-left: 3px solid var(--ce-note);
        }}

        @media (max-width: 980px) {{
            .ce-right-rail {{
                position: static;
            }}

            .ce-quiz-options {{
                grid-template-columns: 1fr;
            }}

            .ce-topbar-row, .ce-footer-row {{
                flex-direction: column;
                align-items: stretch;
            }}

            .ce-top-actions {{
                justify-content: flex-start;
            }}

            .ce-quiz-options {{
                grid-template-columns: 1fr;
            }}
        }}

        @media (max-width: 720px) {{
            .ce-hero, .ce-topbar, .ce-card, .ce-side-card, .ce-progress-card, .ce-footer {{
                border-radius: 12px;
            }}

            .ce-card, .ce-hero, .ce-topbar, .ce-footer {{
                padding: 0.9rem;
            }}

            .ce-quiz-card::after {{
                top: auto;
                bottom: 0.85rem;
            }}
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )
