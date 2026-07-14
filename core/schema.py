"""Pydantic models representing the canonical LLM response schema.

These models are intentionally strict: all fields are required and
typed so downstream code can rely on a consistent structure regardless
of the raw LLM output.
"""
from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class ComplexityModel(BaseModel):
    """Represents a time/space complexity annotation.

    Attributes:
        value: Big-O style complexity (e.g. "O(n)").
        explanation: Short explanation describing why the complexity
            applies to the submitted code.
    """

    value: str = Field(..., description="Big-O style complexity, e.g. 'O(n)'")
    explanation: str = Field(..., description="Why this complexity applies")


class LineByLineItem(BaseModel):
    """Per-line explanation produced by the LLM.

    Attributes:
        line_number: 1-based line number in the original snippet.
        code: The exact source code for this line.
        explanation: Plain-English explanation for the line.
    """

    line_number: int = Field(..., ge=1)
    code: str = Field(...)
    explanation: str = Field(...)


class QuizItem(BaseModel):
    """A short quiz item to test the user's understanding.

    Attributes:
        question: The quiz question text.
        options: Ordered list of answer options.
        correct_answer: The correct option (value exactly matching one
            of the entries in `options`).
        explanation: Short explanation for the correct answer.
    """

    question: str = Field(...)
    options: List[str] = Field(..., min_items=1)
    correct_answer: str = Field(...)
    explanation: str = Field(...)


class AnalysisResult(BaseModel):
    """Top-level analysis result returned to the UI.

    Fields:
        detected_language: Language detected or asserted for the snippet.
        summary: One-paragraph plain-English summary of the code's purpose.
        time_complexity: ComplexityModel describing time complexity.
        space_complexity: ComplexityModel describing space complexity.
        line_by_line: Ordered list of per-line explanations.
        improvements: List of suggested improvements or refactorings.
        quiz: A short quiz to check understanding.
    """

    detected_language: str = Field(..., description="Detected programming language")
    summary: str = Field(..., description="Plain-English summary of the snippet")
    time_complexity: ComplexityModel = Field(...)
    space_complexity: ComplexityModel = Field(...)
    line_by_line: List[LineByLineItem] = Field(..., min_items=0)
    improvements: List[str] = Field(..., description="Suggested improvements")
    quiz: List[QuizItem] = Field(..., min_items=1)

