"""core.parser
Parsing utilities for normalizing raw LLM responses into Python dicts.

Responsibilities:
- Accept a raw LLM response (string or dict-like).
- If a string, parse JSON into a dict using `json.loads`.
- If parsing fails, raise `MalformedJSONError`.
- Never perform schema validation or modify field names/values.
"""
from __future__ import annotations

import json
import re
from typing import Any, Dict, Union


class ParserError(Exception):
    """Base class for parser errors."""


class MalformedJSONError(ParserError):
    """Raised when the LLM returned invalid JSON that cannot be parsed."""


class UnsupportedResponseTypeError(ParserError):
    """Raised when the response type is not supported by the parser."""


def parse_llm_response(response: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Normalize a raw LLM response into a plain Python dict.

    Args:
        response: Raw response from the LLM. If a dict is provided it is
            returned unchanged. If a string is provided it is parsed as
            JSON via `json.loads`.

    Returns:
        A Python dictionary representing the parsed JSON.

    Raises:
        MalformedJSONError: If the input is a string but not valid JSON.
        UnsupportedResponseTypeError: If the input is neither `str` nor `dict`.

    Notes:
    - This function does NOT perform any schema validation or normalization
      beyond converting JSON text into a dict. Validation is the
      responsibility of the `validator` module.
    - The function intentionally does not modify, rename, or fill any fields.
    """
    # If it's already a dict-like object, return as-is
    if isinstance(response, dict):
        return response

    # Accept JSON strings and parse them
    if isinstance(response, str):
        raw = response

        # Strip BOM and surrounding whitespace
        raw = raw.lstrip("\ufeff").strip()

        # If the model wrapped the JSON in a Markdown code fence (``` or ~~~),
        # extract the fenced content. This handles fences with an optional
        # language hint such as ```json.
        fence_match = re.search(r"(?:```|~~~)\s*(?:\w+)?\s*\n(.*?)(?:\n(?:```|~~~))", raw, flags=re.DOTALL)
        if fence_match:
            candidate = fence_match.group(1).strip()
        else:
            candidate = raw

        # First, try the straightforward parse on the candidate text
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            # As a conservative fallback, try to locate the first balanced
            # JSON object substring in the candidate text. We only attempt
            # to extract substrings that begin with '{' and end with the
            # matching '}' and test each with json.loads. This does NOT
            # attempt to repair malformed JSON — it only extracts a valid
            # JSON object if one exists verbatim inside the text.
            s = candidate
            found = None
            for start_idx, ch in enumerate(s):
                if ch != '{':
                    continue
                depth = 0
                for end_idx in range(start_idx, len(s)):
                    if s[end_idx] == '{':
                        depth += 1
                    elif s[end_idx] == '}':
                        depth -= 1
                        if depth == 0:
                            sub = s[start_idx : end_idx + 1]
                            try:
                                parsed_sub = json.loads(sub)
                            except json.JSONDecodeError:
                                # Not a valid JSON object; continue searching
                                break
                            if isinstance(parsed_sub, dict):
                                found = parsed_sub
                                break
                if found is not None:
                    break

            if found is not None:
                return found

            # Nothing parseable found — raise original error
            raise MalformedJSONError("Failed to parse JSON from LLM response")

        if not isinstance(parsed, dict):
            # Parsed JSON may be a list or primitive; surface that as an error
            raise MalformedJSONError("Parsed JSON is not an object/dict")

        return parsed

    # Unsupported type
    raise UnsupportedResponseTypeError(
        f"Unsupported response type: {type(response).__name__}. Expected str or dict."
    )
