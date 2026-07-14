"""Prompt loader and renderer.

This module loads prompt templates from the `prompts/` directory and
provides helper functions to render them with the appropriate
placeholders. Prompts themselves are stored as plain text files so
operators can edit them without touching Python code.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict


PROMPTS_DIR = Path(__file__).resolve().parents[1] / "prompts"


def _load_prompt_file(name: str) -> str:
    """Load a prompt text file from the `prompts/` directory.

    Args:
        name: File name under the prompts directory (e.g. 'user_prompt.txt').

    Returns:
        The file contents as a string.

    Raises:
        FileNotFoundError: If the prompt file does not exist.
    """
    path = PROMPTS_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    return path.read_text(encoding="utf-8")


def load_system_prompt() -> str:
    """Return the system prompt text.

    The system prompt defines global rules and the required JSON schema.
    """
    return _load_prompt_file("system_prompt.txt")


def load_repair_prompt() -> str:
    """Return the repair prompt text used to fix invalid JSON output."""
    return _load_prompt_file("repair_prompt.txt")


def build_user_prompt(code: str, language: str, difficulty: str) -> str:
    """Render the user prompt by replacing placeholders.

    Supported placeholders in the template:
    - {{CODE}}
    - {{LANGUAGE}}
    - {{DIFFICULTY}}

    Args:
        code: The source code to insert.
        language: Explanation language ('English' or 'Hindi').
        difficulty: Difficulty level ('Beginner', 'Intermediate', 'Advanced').

    Returns:
        Rendered prompt text ready to send to the LLM.
    """
    template = _load_prompt_file("user_prompt.txt")
    prompt = template.replace("{{CODE}}", code)
    prompt = prompt.replace("{{LANGUAGE}}", language)
    prompt = prompt.replace("{{DIFFICULTY}}", difficulty)
    return prompt


def load_all_prompts() -> Dict[str, str]:
    """Return a dict with all prompt texts (system, user template, repair).

    Useful for debugging or previewing prompts.
    """
    return {
        "system": load_system_prompt(),
        "user_template": _load_prompt_file("user_prompt.txt"),
        "repair": load_repair_prompt(),
    }
