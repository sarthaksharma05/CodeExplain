"""Validation helpers using Pydantic models from :mod:`core.schema`.

This module exposes a small validation API that converts raw JSON-like
objects into strongly typed Pydantic models. It intentionally does not
depend on Streamlit or any UI framework.
"""
from __future__ import annotations

from typing import Any, Type

from pydantic import ValidationError, BaseModel

from .schema import AnalysisResult


class InvalidResponseError(Exception):
    """Raised when an LLM response cannot be validated.

    The exception message contains details about which fields failed
    validation to aid debugging and monitoring.
    """


def validate_json(data: Any, model: Type[BaseModel]) -> BaseModel:
    """Validate `data` against the provided Pydantic `model`.

    Args:
        data: The JSON-like object (dict) to validate.
        model: Pydantic model class to validate against.

    Returns:
        An instance of `model` populated with validated data.

    Raises:
        InvalidResponseError: when validation fails. The original
            ``pydantic.ValidationError`` is attached as the __cause__.
    """
    try:
        return model.parse_obj(data)
    except ValidationError as exc:
        # Provide a concise, actionable message for callers and logs
        raise InvalidResponseError(f"Validation failed: {exc}") from exc


def validate_analysis(data: Any) -> AnalysisResult:
    """Validate raw LLM output and return an `AnalysisResult`.

    This function centralizes validation for the application's primary
    response type.

    Args:
        data: JSON-like dictionary expected to conform to
            :class:`core.schema.AnalysisResult`.

    Returns:
        Validated :class:`core.schema.AnalysisResult` instance.

    Raises:
        InvalidResponseError: when the provided data does not match the
            required schema.
    """
    # Ensure `quiz` is always a list for downstream consumers.
    # If the LLM returned a single quiz object (dict), wrap it into a list.
    if isinstance(data, dict) and "quiz" in data and not isinstance(data["quiz"], list):
        data = dict(data)  # shallow copy to avoid mutating caller data
        data["quiz"] = [data["quiz"]]
    return validate_json(data=data, model=AnalysisResult)

