"""core.groq_client
Groq API client wrapper.

This module implements a small, self-contained client that handles:
- loading configuration from the environment (via python-dotenv),
- creating an instance of the official Groq client (when available),
- sending prompts and returning the raw text response.

Design goals:
- Keep the client independent from Streamlit and the rest of the app.
- Provide clear exceptions for common failure modes.
- Make it straightforward to replace this implementation with another
  provider by modifying this single module.
"""
from __future__ import annotations

import os
from typing import Any, Dict, Optional, Sequence

from dotenv import load_dotenv


class GroqClientError(Exception):
    """Base class for Groq client errors."""


class MissingAPIKeyError(GroqClientError):
    """Raised when no GROQ_API_KEY is present in the environment."""


class GroqAuthError(GroqClientError):
    """Raised when the API reports an authentication error."""


class GroqRateLimitError(GroqClientError):
    """Raised when the API reports a rate limit or throttling error."""


class GroqTimeoutError(GroqClientError):
    """Raised when the request times out."""


class GroqConnectionError(GroqClientError):
    """Raised for connectivity-related issues (DNS, connection refused)."""


class GroqAPIError(GroqClientError):
    """Generic API error for unexpected responses from Groq."""


class GroqClient:
    """Lightweight wrapper around the Groq SDK/client.

    The client only communicates with the Groq API and returns the raw
    textual response. It intentionally does not perform parsing or
    validation; that responsibility belongs to the parser/validator
    layers.

    Configuration is loaded from environment variables. See
    `.env.example` for available settings.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        timeout: int = 30,
    ) -> None:
        """Initialize the Groq client.

        Args:
            api_key: Explicit API key to use (overrides env var).
            model: Model name to request (overrides env var).
            temperature: Sampling temperature (overrides env var).
            max_tokens: Maximum tokens to request (overrides env var).
            timeout: Network timeout in seconds.
        """
        # Streamlit keeps one Python process alive across reruns, so allow
        # edits to .env to replace values loaded by an earlier run.
        load_dotenv(override=True)

        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise MissingAPIKeyError("GROQ_API_KEY is required but not set")

        self.model = model or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        try:
            self.temperature = (
                float(temperature)
                if temperature is not None
                else float(os.getenv("GROQ_TEMPERATURE", "0.2"))
            )
        except ValueError:
            self.temperature = 0.2

        try:
            self.max_tokens = (
                int(max_tokens)
                if max_tokens is not None
                else int(os.getenv("GROQ_MAX_TOKENS", "4096"))
            )
        except ValueError:
            self.max_tokens = 4096

        self.timeout = timeout
        self._client = None

    def _ensure_client(self):
        """Lazily import and instantiate the Groq SDK client.

        This defers the heavy import/initialization to the moment a request
        is actually made, and provides a clearer error message if the
        installed `groq` package is incompatible.
        """
        if self._client is not None:
            return self._client

        try:
            # Import the official Groq client (v1.x)
            from groq import Groq  # type: ignore
        except Exception as exc:  # pragma: no cover - environment dependent
            raise GroqAPIError(
                "Failed to import the 'groq' package. Ensure groq v1.x is installed."
            ) from exc

        try:
            client = Groq(api_key=self.api_key)
        except Exception as exc:
            raise GroqAPIError("Failed to instantiate Groq(api_key=...) client") from exc

        self._client = client
        return self._client

    def send_prompt(self, system_prompt: str, user_prompt: str) -> str:
        """Send a prompt to the Groq API and return the raw text response.

        Args:
            system_prompt: System-level instructions for the model.
            user_prompt: The user's prompt or code to analyze.

        Returns:
            Raw response text from Groq.

        Raises:
            GroqAuthError: on authentication failures.
            GroqRateLimitError: when rate limited.
            GroqTimeoutError: on network timeouts.
            GroqConnectionError: on connection failures.
            GroqAPIError: on other API errors.
        """
        # Strictly use Groq v1.x client API: client.chat.completions.create(...)
        client = self._ensure_client()
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                timeout=self.timeout,
            )
        except Exception as exc:  # pragma: no cover - depends on runtime API
            msg = str(exc).lower()
            if "401" in msg or "unauthor" in msg:
                raise GroqAuthError("Authentication with Groq failed") from exc
            if "rate" in msg or "throttl" in msg:
                raise GroqRateLimitError("Groq rate limit exceeded") from exc
            if "timeout" in msg:
                raise GroqTimeoutError("Request to Groq timed out") from exc
            if "connection" in msg or "failed to establish a new connection" in msg:
                raise GroqConnectionError("Failed to connect to Groq API") from exc
            raise GroqAPIError("Unexpected error while calling Groq API") from exc

        # Per Groq v1.x SDK, return only response.choices[0].message.content
        try:
            return response.choices[0].message.content
        except Exception as exc:
            raise GroqAPIError("Failed to extract text from Groq response") from exc

