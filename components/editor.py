from __future__ import annotations

import time
import json
import streamlit as st

from core.agent import GroqRequestError, ParseError, RepairFailedError
from core.groq_client import GroqAuthError, GroqRateLimitError, GroqTimeoutError, GroqConnectionError

try:
    from streamlit_ace import st_ace
except Exception:  # pragma: no cover - fallback for environments without the component
    st_ace = None

SUPPORTED_LANGUAGES = ["Auto Detect", "Python", "Java", "C++", "JavaScript", "C", "Go", "Rust"]
OUTPUT_LANGUAGES = ["English", "हिन्दी"]
SAMPLE_CODE = {
    "Auto Detect": "def greet(name):\n    return f\"Hello, {name}!\"\n\nprint(greet('CodeExplain'))",
    "Python": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)",
    "Java": "class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, CodeExplain\");\n    }\n}",
    "C++": "#include <iostream>\nusing namespace std;\n\nint main() {\n    cout << \"Hello, CodeExplain\" << endl;\n    return 0;\n}",
    "JavaScript": "function greet(name) {\n  return `Hello, ${name}!`;\n}\nconsole.log(greet('CodeExplain'));",
    "C": "#include <stdio.h>\n\nint main() {\n    printf(\"Hello, CodeExplain\\n\");\n    return 0;\n}",
    "Go": "package main\n\nimport \"fmt\"\n\nfunc main() {\n    fmt.Println(\"Hello, CodeExplain\")\n}",
    "Rust": "fn main() {\n    println!(\"Hello, CodeExplain\");\n}",
}


def _control(options, key, default):
    segmented = getattr(st, "segmented_control", None)
    if segmented is not None:
        return segmented(
            label="Output language",
            options=options,
            default=default,
            key=key,
            label_visibility="collapsed",
        )
    return st.radio(
        label="Output language",
        options=options,
        index=options.index(default),
        key=key,
        horizontal=True,
        label_visibility="collapsed",
    )


def _ensure_state() -> None:
    st.session_state.setdefault("codeexplain_code", SAMPLE_CODE["Auto Detect"])
    st.session_state.setdefault("codeexplain_language", "Auto Detect")
    st.session_state.setdefault("codeexplain_output_language", "English")
    st.session_state.setdefault("codeexplain_show_progress", False)
    st.session_state.setdefault("codeexplain_copy_notice", "")
    st.session_state.setdefault("codeexplain_is_running", False)
    st.session_state.setdefault("codeexplain_difficulty", "Intermediate")


def _has_cause(exc: Exception, exc_type: type[Exception]) -> bool:
    current: BaseException | None = exc
    while current is not None:
        if isinstance(current, exc_type):
            return True
        current = current.__cause__ or current.__context__
    return False


def _friendly_analysis_error(exc: Exception) -> str:
    if _has_cause(exc, GroqRateLimitError):
        return "Groq rate limit reached. Please wait a few minutes and try again."
    if _has_cause(exc, GroqAuthError):
        return "Groq API authentication failed. Please check your GROQ_API_KEY in .env."
    if _has_cause(exc, GroqTimeoutError):
        return "Groq took too long to respond. Please try again."
    if _has_cause(exc, GroqConnectionError):
        return "Could not connect to Groq. Please check your internet connection and try again."
    if isinstance(exc, GroqRequestError):
        return "Groq could not analyze the code right now. Please try again."
    if isinstance(exc, (ParseError, RepairFailedError)):
        return "The AI response was too short or incomplete. Increase GROQ_MAX_TOKENS in .env and try again."
    return "Unable to analyze the code. Please try again."


def render_editor_card() -> None:
    _ensure_state()

    st.markdown(
        """
                <div class="ce-card">
                    <div class="ce-card-title">Input Code</div>
                    <div class="ce-card-subtitle">Paste code, choose language and translation mode, then read it back as annotated teaching notes.</div>
        """,
        unsafe_allow_html=True,
    )

    col_a, col_b = st.columns([1, 1], gap="large")
    with col_a:
        st.markdown('<span class="ce-label">Language selector</span>', unsafe_allow_html=True)
        language = st.selectbox(
            label="Language",
            options=SUPPORTED_LANGUAGES,
            key="codeexplain_language",
            label_visibility="collapsed",
        )
        st.markdown('<span class="ce-label">Difficulty</span>', unsafe_allow_html=True)
        difficulty = st.selectbox(
            label="Difficulty",
            options=["Beginner", "Intermediate", "Advanced"],
            key="codeexplain_difficulty",
            label_visibility="collapsed",
        )
    with col_b:
        st.markdown('<span class="ce-label">Output language</span>', unsafe_allow_html=True)
        output_language = _control(OUTPUT_LANGUAGES, key="codeexplain_output_language_control", default=st.session_state["codeexplain_output_language"])
        st.session_state["codeexplain_output_language"] = output_language

    st.markdown('<div class="ce-editor-shell">', unsafe_allow_html=True)
    st.markdown('<div class="ce-code-label">Editor</div>', unsafe_allow_html=True)
    editor_theme = "chrome" if st.session_state.get("codeexplain_theme", "Light") == "Light" else "tomorrow_night"
    language_map = {
        "Auto Detect": "python",
        "Python": "python",
        "Java": "java",
        "C++": "cpp",
        "JavaScript": "javascript",
        "C": "c",
        "Go": "golang",
        "Rust": "rust",
    }

    current_code = st.session_state["codeexplain_code"]

    if st_ace is not None:
        edited_code = st_ace(
            value=current_code,
            language=language_map.get(language, "python"),
            theme=editor_theme,
            key="codeexplain_ace_editor",
            height=360,
            min_lines=14,
            show_gutter=True,
            auto_update=True,
            font_size=14,
            tab_size=4,
            placeholder="Paste your code here...",
        )
        if edited_code is not None:
            st.session_state["codeexplain_code"] = edited_code
    else:
        edited_code = st.text_area(
            label="Code Editor",
            value=current_code,
            height=360,
            key="codeexplain_fallback_editor",
            label_visibility="collapsed",
            placeholder="Paste your code here...",
        )
        st.session_state["codeexplain_code"] = edited_code

    st.markdown('</div>', unsafe_allow_html=True)

    button_cols = st.columns([1.3, 0.9, 0.9, 0.9], gap="small")
    with button_cols[0]:
        disabled = st.session_state.get("codeexplain_is_running", False)
        if st.button("Explain Code", type="primary", use_container_width=True, key="codeexplain_explain", disabled=disabled):
            # Retrieve inputs
            agent = st.session_state.get("codeexplain_agent")
            code = st.session_state.get("codeexplain_code", "")
            # Explanation language comes from the output language control
            explanation_language = st.session_state.get("codeexplain_output_language", "English")
            # Normalize output language values (UI may show localized labels)
            if explanation_language == "हिन्दी":
                explanation_language = "Hindi"
            difficulty = st.session_state.get("codeexplain_difficulty", "Intermediate")

            # Empty code validation
            if not code or not code.strip():
                st.warning("Please paste some code before analyzing.")
            else:
                # Mark start time and show progress UI
                st.session_state["codeexplain_is_running"] = True
                st.session_state["codeexplain_show_progress"] = True
                st.session_state["codeexplain_start_ts"] = time.time()
                st.session_state.pop("analysis_error", None)
                st.session_state.pop("codeexplain_success", None)
                try:
                    with st.spinner("🤖 AI Agent Working..."):
                        # Single backend call - pass the explanation language
                        result = agent.analyze_code(code=code, language=explanation_language, difficulty=difficulty)

                    # Store only the validated AnalysisResult (plain dict)
                    st.session_state["analysis_result"] = result
                    # Record response time
                    st.session_state["codeexplain_end_ts"] = time.time()
                    st.session_state["codeexplain_response_time"] = (
                        st.session_state["codeexplain_end_ts"] - st.session_state["codeexplain_start_ts"]
                    )
                    st.session_state.pop("codeexplain_success", None)
                except Exception as exc:
                    # Friendly, non-technical error for users (no debug leakage)
                    st.session_state["analysis_result"] = None
                    message = _friendly_analysis_error(exc)
                    st.session_state["analysis_error"] = message
                finally:
                    st.session_state["codeexplain_is_running"] = False
                    st.session_state["codeexplain_show_progress"] = False
    with button_cols[1]:
        if st.button("Clear", use_container_width=True, key="codeexplain_clear"):
            st.session_state["codeexplain_code"] = ""
            st.session_state["codeexplain_show_progress"] = False
            st.session_state["codeexplain_copy_notice"] = "Cleared editor content."
    with button_cols[2]:
        if st.button("Load Sample", use_container_width=True, key="codeexplain_sample"):
            st.session_state["codeexplain_code"] = SAMPLE_CODE.get(language, SAMPLE_CODE["Auto Detect"])
            st.session_state["codeexplain_show_progress"] = False
            st.session_state["codeexplain_copy_notice"] = f"Loaded sample for {language}."
    with button_cols[3]:
        if st.button("Copy Code", use_container_width=True, key="codeexplain_copy"):
            # Copy to clipboard using a small HTML button fallback
            st.session_state["codeexplain_copy_notice"] = "Code copied to clipboard (browser)."
            st.markdown(
                f"""
                <script>
                navigator.clipboard.writeText({json.dumps(st.session_state.get('codeexplain_code',''))}).then(()=>{{}})
                </script>
                """,
                unsafe_allow_html=True,
            )

    if st.session_state.get("codeexplain_copy_notice"):
        st.caption(st.session_state["codeexplain_copy_notice"])

    st.markdown("</div>", unsafe_allow_html=True)


def render_process_indicator() -> None:
    if not st.session_state.get("codeexplain_show_progress"):
        return

    st.markdown(
        """
        <div class="ce-progress-card">
          <div class="ce-card-title">Processing</div>
          <div class="ce-card-subtitle">UI-only placeholder showing the flow that will run later.</div>
          <div class="ce-progress-list">
            <div class="ce-progress-item"><span class="ce-progress-dot"></span><span class="ce-progress-step">Detecting Language</span><span class="ce-progress-status">Queued</span></div>
            <div class="ce-progress-item"><span class="ce-progress-dot"></span><span class="ce-progress-step">Understanding Logic</span><span class="ce-progress-status">Queued</span></div>
            <div class="ce-progress-item"><span class="ce-progress-dot"></span><span class="ce-progress-step">Calculating Complexity</span><span class="ce-progress-status">Queued</span></div>
            <div class="ce-progress-item"><span class="ce-progress-dot"></span><span class="ce-progress-step">Generating Explanation</span><span class="ce-progress-status">Queued</span></div>
            <div class="ce-progress-item"><span class="ce-progress-dot"></span><span class="ce-progress-step">Creating Quiz</span><span class="ce-progress-status">Queued</span></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
