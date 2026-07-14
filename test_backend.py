"""Standalone backend integration test for CodeExplain.

This script exercises the complete backend pipeline (prompts -> Groq ->
parser -> validator) without touching the Streamlit frontend.

It prints a readable summary of the validated AnalysisResult.
"""
from __future__ import annotations

import json
import sys
from dataclasses import asdict
from typing import Any

from dotenv import load_dotenv

from core.agent import CodeExplainAgent, PromptLoadError, GroqRequestError, ParseError, RepairFailedError
from core.groq_client import MissingAPIKeyError, GroqClientError
from core.schema import AnalysisResult


SAMPLE_CODE = '''def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
'''


def print_analysis(result: AnalysisResult) -> None:
    """Print fields of AnalysisResult in a readable format."""
    data = result.dict() if hasattr(result, "dict") else asdict(result)  # pydantic or dataclass

    print("\n=== Analysis Result ===\n")
    print(f"Detected Language: {data.get('detected_language')}")
    print(f"\nSummary:\n{data.get('summary')}\n")

    tc = data.get("time_complexity", {})
    sc = data.get("space_complexity", {})
    print(f"Time Complexity: {tc.get('value')}")
    print(f"Time Complexity Explanation: {tc.get('explanation')}\n")
    print(f"Space Complexity: {sc.get('value')}")
    print(f"Space Complexity Explanation: {sc.get('explanation')}\n")

    print("Line-by-Line Explanation:")
    for item in data.get("line_by_line", []):
        print(f"  {item.get('line_number')}: {item.get('code')}")
        print(f"     -> {item.get('explanation')}")

    print("\nSuggested Improvements:")
    for i, imp in enumerate(data.get("improvements", []), start=1):
        print(f"  {i}. {imp}")

    quiz = data.get("quiz") or {}
    if quiz:
        print("\nQuiz Question:")
        print(f"  Q: {quiz.get('question')}")
        for idx, opt in enumerate(quiz.get("options", []), start=1):
            print(f"    {idx}. {opt}")
        print(f"  Correct Answer: {quiz.get('correct_answer')}")
        print(f"  Explanation: {quiz.get('explanation')}")


def main() -> int:
    print("Loading environment...")
    load_dotenv()

    print("Creating agent...")
    try:
        agent = CodeExplainAgent()
    except MissingAPIKeyError:
        print("Error: GROQ_API_KEY is missing. Create a .env file with your GROQ_API_KEY.")
        return 2
    except GroqClientError as exc:
        print(f"Groq client initialization error: {exc}")
        return 3
    except Exception as exc:
        print(f"Unexpected error creating agent: {exc}")
        return 4

    print("Loading prompts...")
    print("Sending request to Groq...")
    try:
        result = agent.analyze_code(code=SAMPLE_CODE, language="English", difficulty="Beginner")
    except PromptLoadError as exc:
        print(f"Prompt loading error: {exc}")
        return 5
    except MissingAPIKeyError:
        print("Error: GROQ_API_KEY is missing. Please set it in your .env.")
        return 6
    except GroqRequestError as exc:
        print(f"Groq request failed: {exc}")
        return 7
    except ParseError as exc:
        print(f"Parser error: {exc}")
        return 8
    except RepairFailedError as exc:
        print(f"Repair failed: {exc}")
        return 9
    except Exception as exc:  # catch-all for unexpected orchestration errors
        print(f"Unexpected error during analysis: {exc}")
        return 10

    print("Parsing response...\nValidating response...")

    # Print the validated AnalysisResult
    try:
        print_analysis(result)
    except Exception as exc:
        print(f"Failed to display result: {exc}")
        return 11

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
