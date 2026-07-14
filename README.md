# CodeExplain — Plain-English Code Tutor

An AI-powered Streamlit application that explains code in plain English with complexity analysis, line-by-line breakdowns, improvement suggestions, and interactive quizzes.

## Features

- **Plain-English Explanations** — Paste any code snippet and get a clear, teacher-style walkthrough
- **Complexity Analysis** — Time and space complexity with reasoning
- **Line-by-Line Breakdown** — Every line annotated like a teacher's margin note
- **Improvement Suggestions** — Actionable refactoring tips
- **Interactive Quiz** — Test your understanding with auto-generated questions
- **Multi-Language Support** — Explanations in English or Hindi
- **Syntax-Highlighted Editor** — Ace-powered editor with 8 language modes
- **Export Options** — Download results as JSON or PDF

## Tech Stack

- Python · Streamlit · streamlit-ace
- Groq API (LLaMA 3.3 70B)
- Pydantic (response validation)

## Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/sarthaksharma05/CodeExplain.git
cd CodeExplain

# 2. Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# 5. Run the app
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → select this repository
4. Set **Main file path** to `app.py`
5. Open **Advanced settings** → **Secrets** and add:
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   GROQ_MODEL = "llama-3.3-70b-versatile"
   GROQ_TEMPERATURE = "0.2"
   GROQ_MAX_TOKENS = "4096"
   ```
6. Click **Deploy**

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `GROQ_API_KEY` | ✅ Yes | — | Your Groq API key |
| `GROQ_MODEL` | No | `llama-3.3-70b-versatile` | Model to use |
| `GROQ_TEMPERATURE` | No | `0.2` | Sampling temperature |
| `GROQ_MAX_TOKENS` | No | `4096` | Max response tokens |

These can be set via a `.env` file (local) or Streamlit Secrets (cloud).

## Project Structure

```
├── app.py                  # Entry point
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml         # Streamlit theme & server config
├── components/             # UI components
│   ├── editor.py           # Code editor + Explain button
│   ├── hero.py             # Hero section
│   ├── navbar.py           # Top navigation
│   ├── sidebar.py          # Right info rail
│   ├── tabs.py             # Results tabs (explanation, quiz, etc.)
│   └── footer.py           # Footer
├── core/                   # Backend logic
│   ├── agent.py            # Orchestrator (prompt → LLM → parse → validate)
│   ├── groq_client.py      # Groq API client
│   ├── parser.py           # JSON response parser
│   ├── validator.py        # Pydantic validation
│   ├── schema.py           # Response schema models
│   └── prompts.py          # Prompt loader
├── prompts/                # Prompt templates (plain text)
│   ├── system_prompt.txt
│   ├── user_prompt.txt
│   └── repair_prompt.txt
├── styles.py               # Global CSS injection
└── assets/
    └── logo.svg
```

## License

MIT
