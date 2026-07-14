from __future__ import annotations

import streamlit as st
import json
import io
import time


def render_results_tabs() -> None:
    st.markdown('<div class="ce-tab-shell">', unsafe_allow_html=True)
    tabs = st.tabs(["Explanation", "Complexity", "Line-by-Line", "Improvements", "Quiz"])
    result = st.session_state.get("analysis_result")
    response_time = st.session_state.get("codeexplain_response_time")
    start_ts = st.session_state.get("codeexplain_start_ts")
    end_ts = st.session_state.get("codeexplain_end_ts")
    error = st.session_state.get("analysis_error")

    # Helper: copy button using JS 
    def _copy_button(payload: str, label: str = "Copy"):
        safe = json.dumps(payload)
        html = f"<button class='ce-copy-button' onclick='navigator.clipboard.writeText({safe})'>{label}</button>"
        st.markdown(html, unsafe_allow_html=True)

    # Helper: download JSON
    def _download_json(obj, filename="analysis.json", key="analysis_json"):
        data = json.dumps(obj, ensure_ascii=False, indent=2)
        st.download_button(label="Download JSON", data=data, file_name=filename, mime="application/json", key=key)

    # Helper: PDF export (best-effort)
    def _download_pdf(obj, key="analysis_pdf"):
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas

            buf = io.BytesIO()
            c = canvas.Canvas(buf, pagesize=letter)
            text = c.beginText(40, 750)
            text.setFont("Helvetica", 10)
            lines = json.dumps(obj, indent=2, ensure_ascii=False).splitlines()
            for line in lines:
                text.textLine(line[:90])
                if text.getY() < 40:
                    c.drawText(text)
                    c.showPage()
                    text = c.beginText(40, 750)
                    text.setFont("Helvetica", 10)
            c.drawText(text)
            c.save()
            buf.seek(0)
            st.download_button(label="Download PDF", data=buf, file_name="analysis.pdf", mime="application/pdf", key=key)
        except Exception:
            st.button("Download PDF", disabled=True, key=f"{key}_disabled")

    # NOTE: The application uses a single, strict contract: the backend
    # returns a plain Python dict matching the agreed AnalysisResult schema.
    # The UI assumes only dicts/lists; no compatibility shims are used here.
    required_result_keys = {
        "summary",
        "time_complexity",
        "space_complexity",
        "line_by_line",
        "improvements",
        "quiz",
    }
    result_is_complete = isinstance(result, dict) and required_result_keys.issubset(result)
    if result is not None and not result_is_complete:
        result = None
        error = error or "Unable to display the analysis result. Please run the analysis again."

    with tabs[0]:
        st.markdown('<div class="ce-card">', unsafe_allow_html=True)
        st.markdown('<div class="ce-card-title">Explanation</div>', unsafe_allow_html=True)
        if error:
            # Professional error card
            st.markdown('<div class="ce-card">', unsafe_allow_html=True)
            st.markdown(f"<div class=\"ce-card-title\">Analysis Error</div>", unsafe_allow_html=True)
            # Show a friendly, non-technical message to users
            st.error(error)
            st.markdown('<div style="margin-top:0.5rem">Try simplifying the input, reducing file size, or retrying.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        elif result is None:
            # Professional empty state
            if error:
                st.error("Unable to display the analysis result. Please run the analysis again.")
            else:
                st.markdown('<div class="ce-placeholder-box">Paste your code on the left and click <strong>Explain Code</strong> to get a plain-English walkthrough, complexity, and a short quiz.</div>', unsafe_allow_html=True)
        else:
            # `summary` is expected to be a plain string
            st.markdown(f"<div class=\"ce-explanation\">{result['summary']}</div>", unsafe_allow_html=True)
            # Copy / Download row
            cols = st.columns([1, 0.6, 0.6])
            with cols[0]:
                _copy_button(result['summary'], label='Copy Summary')
            with cols[1]:
                _download_json({'summary': result['summary']}, filename='summary.json', key='summary_json')
            with cols[2]:
                _download_pdf({'summary': result['summary']}, key='summary_pdf')
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[1]:
        left, right = st.columns(2, gap="large")
        with left:
            st.markdown('<div class="ce-card">', unsafe_allow_html=True)
            st.markdown('<div class="ce-card-title">Time Complexity</div>', unsafe_allow_html=True)
            if result is None:
                st.markdown('<div class="ce-placeholder-box">Big-O reasoning will appear here as a margin annotation, not a metric tile.</div>', unsafe_allow_html=True)
            else:
                tc = result['time_complexity']
                st.markdown(f"<div class=\"ce-note-kicker\">Value</div><div class=\"ce-explanation\">{tc['value']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class=\"ce-note-kicker\">Explanation</div><div class=\"ce-explanation\">{tc['explanation']}</div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with right:
            st.markdown('<div class="ce-card">', unsafe_allow_html=True)
            st.markdown('<div class="ce-card-title">Space Complexity</div>', unsafe_allow_html=True)
            if result is None:
                st.markdown('<div class="ce-placeholder-box">Space reasoning will appear here in the same editorial language.</div>', unsafe_allow_html=True)
            else:
                sc = result['space_complexity']
                st.markdown(f"<div class=\"ce-note-kicker\">Value</div><div class=\"ce-explanation\">{sc['value']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class=\"ce-note-kicker\">Explanation</div><div class=\"ce-explanation\">{sc['explanation']}</div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with tabs[2]:
        st.markdown('<div class="ce-card">', unsafe_allow_html=True)
        st.markdown('<div class="ce-card-title">Line-by-Line</div>', unsafe_allow_html=True)
        st.markdown('<div class="ce-card-subtitle">Each future line will appear like a teacher’s marginal note beside the code.</div>', unsafe_allow_html=True)
        st.markdown('<div class="ce-note-rail" style="max-height: 420px; overflow: auto; padding-right: 0.2rem;">', unsafe_allow_html=True)
        if result is None or not result['line_by_line']:
            st.markdown('<div class="ce-placeholder-box">Line-by-line annotations will appear here.</div>', unsafe_allow_html=True)
        else:
            # Add copy/download for full line-by-line
            cols = st.columns([1, 0.6, 0.6])
            with cols[0]:
                _copy_button('\n'.join([f"Line {i['line_number']}: {i['code']} - {i['explanation']}" for i in result['line_by_line']]), label='Copy Line-by-Line')
            with cols[1]:
                _download_json({'line_by_line': result['line_by_line']}, filename='line_by_line.json', key='line_by_line_json')
            with cols[2]:
                _download_pdf({'line_by_line': result['line_by_line']}, key='line_by_line_pdf')
            for item in result['line_by_line']:
                line_no = item['line_number']
                code = item['code']
                explanation = item['explanation']
                with st.expander(f"Line {line_no}: {code}"):
                    st.markdown(f"<div class=\"ce-note-kicker\">Explanation</div><div class=\"ce-explanation\">{explanation}</div>", unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    with tabs[3]:
        st.markdown('<div class="ce-card">', unsafe_allow_html=True)
        st.markdown('<div class="ce-card-title">Improvements</div>', unsafe_allow_html=True)
        st.markdown('<div class="ce-card-subtitle">Suggestions will read like annotated revision notes rather than generic action items.</div>', unsafe_allow_html=True)
        if result is None or not result['improvements']:
            st.markdown('<div class="ce-placeholder-box">Improvement suggestions will appear here.</div>', unsafe_allow_html=True)
        else:
            cols = st.columns([1, 0.6, 0.6])
            with cols[0]:
                _copy_button('\n'.join(result['improvements']), label='Copy Improvements')
            with cols[1]:
                _download_json({'improvements': result['improvements']}, filename='improvements.json', key='improvements_json')
            with cols[2]:
                _download_pdf({'improvements': result['improvements']}, key='improvements_pdf')
            for idx, suggestion in enumerate(result['improvements'], start=1):
                key = f"improve_{idx}"
                checked = st.checkbox(label=suggestion, key=key)
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[4]:
        st.markdown('<div class="ce-card">', unsafe_allow_html=True)
        st.markdown('<div class="ce-card-title">Quiz</div>', unsafe_allow_html=True)
        if result is None or not result['quiz']:
            st.markdown('<div class="ce-placeholder-box">Quiz will appear here.</div>', unsafe_allow_html=True)
        else:
            cols = st.columns([1, 0.6, 0.6])
            with cols[0]:
                _copy_button('\n'.join([q['question'] for q in result['quiz']]), label='Copy Quiz')
            with cols[1]:
                _download_json({'quiz': result['quiz']}, filename='quiz.json', key='quiz_json')
            with cols[2]:
                _download_pdf({'quiz': result['quiz']}, key='quiz_pdf')
            quiz_list = result['quiz']
            for q_idx, q in enumerate(quiz_list, start=1):
                st.markdown(f'<div class="ce-quiz-card"><div class="ce-note-kicker">Question {q_idx}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="ce-quiz-question">{q["question"]}</div>', unsafe_allow_html=True)
                options = q['options']
                choice_key = f"quiz_{q_idx}_choice"
                st.session_state.setdefault(choice_key, None)
                selected = st.radio(
                    label=f"Answer for question {q_idx}",
                    options=options,
                    key=choice_key,
                    label_visibility="collapsed",
                )
                reveal_key = f"quiz_{q_idx}_reveal"
                if st.button("Reveal Answer", key=reveal_key):
                    correct = q['correct_answer']
                    st.markdown(f"**Correct Answer:** {correct}")
                    if q.get('explanation'):
                        st.markdown(f"**Explanation:** {q['explanation']}")
                st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Side strip: statistics and response time
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="ce-side-card">', unsafe_allow_html=True)
    st.markdown('<div class="ce-card-title">Analysis Summary</div>', unsafe_allow_html=True)
    code = st.session_state.get('codeexplain_code','')
    loc = len(code.splitlines()) if code else 0
    language = st.session_state.get('codeexplain_language','Auto Detect')
    difficulty = st.session_state.get('codeexplain_difficulty','Intermediate')
    explanation_language = st.session_state.get('codeexplain_output_language','English')
    st.markdown(f'<div class="ce-side-item"><strong>Language:</strong> {language}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="ce-side-item"><strong>Lines of Code:</strong> {loc}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="ce-side-item"><strong>Difficulty:</strong> {difficulty}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="ce-side-item"><strong>Explanation Language:</strong> {explanation_language}</div>', unsafe_allow_html=True)
    if response_time:
        st.markdown(f'<div style="margin-top:0.6rem" class="ce-pill">Response time: {response_time:.2f}s</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
