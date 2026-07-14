"""core.agent
Orchestrator for CodeExplain backend workflows.

This module contains the `CodeExplainAgent` class which coordinates prompt
creation, LLM request orchestration (through `GroqClient`), response parsing,
and validation. Implementation details are intentionally left as placeholders
so the AI-provider integration can be completed in a later step.
"""
from __future__ import annotations

from typing import Optional, Any, Dict
import logging
import json

from .schema import AnalysisResult
from .groq_client import GroqClient, GroqClientError
from . import prompts
# Import parser and validator lazily inside analyze_code to avoid circular
# import issues when the package is imported.


logger = logging.getLogger(__name__)


class AgentError(Exception):
    """Base class for agent-level exceptions."""


class PromptLoadError(AgentError):
    """Raised when prompt files cannot be loaded."""


class GroqRequestError(AgentError):
    """Raised when an error occurs while calling the Groq API."""


class ParseError(AgentError):
    """Raised when the parser cannot interpret the Groq response."""


class RepairFailedError(AgentError):
    """Raised when automatic repair of invalid JSON does not succeed."""


class CodeExplainAgent:
    """Orchestrates the analysis workflow without embedding business logic.

    The agent coordinates prompt loading, sending prompts to the Groq
    client, parsing raw responses, and validating the parsed output.
    It does not perform parsing, validation, or API communication itself;
    those responsibilities are delegated to the respective modules.
    """

    def __init__(self, client: Optional[GroqClient] = None) -> None:
        self._client = client

    def _ensure_client(self) -> GroqClient:
        if self._client is None:
            self._client = GroqClient()
        return self._client

    def analyze_code(self, code: str, language: str, difficulty: str) -> Dict[str, Any]:
        """Run the end-to-end orchestration for analyzing code.

        Args:
            code: Source code to analyze.
            language: Desired explanation language (e.g. 'English', 'Hindi').
            difficulty: Difficulty level ('Beginner', 'Intermediate', 'Advanced').

        Returns:
            dict: Validated analysis result converted to plain Python objects
                via Pydantic `model_dump()` (JSON-compatible dict/lists).

        Raises:
            AgentError: For any orchestration-level failures.
        """
        logger.info("Loading prompts...")
        try:
            system_prompt = prompts.load_system_prompt()
            user_prompt = prompts.build_user_prompt(code=code, language=language, difficulty=difficulty)
        except FileNotFoundError as exc:
            logger.exception("Failed to load prompt files")
            raise PromptLoadError("Failed to load prompt files") from exc

        client = self._ensure_client()

        # First attempt
        logger.info("Calling Groq for initial response...")
        try:
            raw = client.send_prompt(system_prompt=system_prompt, user_prompt=user_prompt)
        except GroqClientError as exc:
            logger.exception("Groq client error during initial request")
            raise GroqRequestError("Groq request failed") from exc

        # Parse (import lazily to avoid circular imports)
        # Log a short debug-level excerpt of the raw response (no stdout prints)
        try:
            logger.debug("Raw Groq response (excerpt): %s", raw[:1000])
        except Exception:
            logger.debug("Failed to log raw Groq response")

        logger.info("Parsing response...")
        try:
            from . import parser as llm_parser  # type: ignore

            parsed = llm_parser.parse_llm_response(raw)
        except Exception as exc:
            logger.exception("Parser error")
            raise ParseError("Failed to parse Groq response") from exc

        # Validate (import lazily)
        logger.info("Validating response...")
        try:
            from . import validator  # type: ignore

            validated = validator.validate_analysis(parsed)
            logger.info("Validation successful.")
            # Convert validated Pydantic model to plain Python dict
            try:
                result_dict = validated.model_dump()
            except Exception as exc:
                logger.exception("Failed to dump validated model to dict")
                raise AgentError("Failed to convert validated model to dict") from exc
            if not isinstance(result_dict, dict):
                raise AgentError("Validated model_dump() did not return a dict")
            return result_dict
        except Exception as first_exc:
            logger.warning("Validation failed: attempting repair")

        # Repair attempt using repair prompt
        logger.info("Loading repair prompt...")
        try:
            repair_prompt = prompts.load_repair_prompt()
        except FileNotFoundError as exc:
            logger.exception("Repair prompt file missing")
            raise PromptLoadError("Repair prompt file missing") from exc

        # Send repair instruction + original raw response to Groq
        repair_user = f"{repair_prompt}\n\nInvalid JSON:\n{raw}"
        logger.info("Calling Groq for repair attempt...")
        try:
            repaired_raw = client.send_prompt(system_prompt=system_prompt, user_prompt=repair_user)
        except GroqClientError as exc:
            logger.exception("Groq client error during repair request")
            raise GroqRequestError("Groq repair request failed") from exc

        # Log a short debug-level excerpt of the repaired response
        try:
            logger.debug("Repaired Groq response (excerpt): %s", repaired_raw[:1000])
        except Exception:
            logger.debug("Failed to log repaired Groq response")

        logger.info("Parsing repaired response...")
        try:
            from . import parser as llm_parser  # type: ignore

            repaired_parsed = llm_parser.parse_llm_response(repaired_raw)
        except Exception as exc:
            logger.exception("Parser error on repaired response")
            raise ParseError("Failed to parse repaired Groq response") from exc

        logger.info("Validating repaired response...")
        try:
            from . import validator  # type: ignore

            final = validator.validate_analysis(repaired_parsed)
            logger.info("Repair validation successful.")
            # Convert validated Pydantic model to plain Python dict
            try:
                result_dict = final.model_dump()
            except Exception as exc:
                logger.exception("Failed to dump repaired model to dict")
                raise AgentError("Failed to convert repaired model to dict") from exc
            if not isinstance(result_dict, dict):
                raise AgentError("Repaired model_dump() did not return a dict")
            return result_dict
        except Exception as exc:
            logger.exception("Repaired response failed validation")
            raise RepairFailedError("Repaired response failed validation") from exc
