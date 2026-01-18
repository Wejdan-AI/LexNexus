"""
WejdanAI Base Provider
=======================
Abstract base class for all AI model providers.
"""

import asyncio
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, AsyncIterator, Optional

import httpx

from ..config.models import ModelConfig, ModelProvider


@dataclass
class Message:
    """A single message in a conversation."""
    role: str  # "user", "assistant", "system"
    content: str
    images: list[str] = field(default_factory=list)  # Base64 or URLs
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class CompletionResponse:
    """Response from an AI model."""
    content: str
    model: str
    provider: ModelProvider
    usage: dict[str, int] = field(default_factory=dict)
    latency_ms: float = 0.0
    citations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    success: bool = True


class BaseProvider(ABC):
    """
    Abstract base class for AI model providers.
    All provider implementations must inherit from this class.
    """

    def __init__(
        self,
        config: ModelConfig,
        api_key: Optional[str] = None,
        timeout: float = 60.0,
        max_retries: int = 3,
    ):
        self.config = config
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self._client: Optional[httpx.AsyncClient] = None
        self._last_request_time: float = 0
        self._request_count: int = 0

    @property
    def client(self) -> httpx.AsyncClient:
        """Get or create the HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(self.timeout),
                headers=self._get_headers(),
            )
        return self._client

    def _get_headers(self) -> dict[str, str]:
        """Get the default headers for API requests."""
        return {
            "Content-Type": "application/json",
        }

    async def close(self):
        """Close the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None

    async def _rate_limit(self):
        """Apply rate limiting based on RPM."""
        if self.config.rate_limit_rpm <= 0:
            return

        min_interval = 60.0 / self.config.rate_limit_rpm
        elapsed = time.time() - self._last_request_time

        if elapsed < min_interval:
            await asyncio.sleep(min_interval - elapsed)

        self._last_request_time = time.time()
        self._request_count += 1

    async def _retry_with_backoff(
        self,
        func,
        *args,
        **kwargs,
    ) -> Any:
        """Execute a function with exponential backoff retry."""
        last_error = None

        for attempt in range(self.max_retries):
            try:
                return await func(*args, **kwargs)
            except httpx.HTTPStatusError as e:
                last_error = e
                if e.response.status_code in (429, 500, 502, 503, 504):
                    wait_time = (2 ** attempt) * 1.0
                    await asyncio.sleep(wait_time)
                else:
                    raise
            except (httpx.ConnectError, httpx.ReadTimeout) as e:
                last_error = e
                wait_time = (2 ** attempt) * 1.0
                await asyncio.sleep(wait_time)

        raise last_error

    @abstractmethod
    async def complete(
        self,
        messages: list[Message],
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> CompletionResponse:
        """
        Generate a completion for the given messages.

        Args:
            messages: List of conversation messages
            system_prompt: Optional system prompt
            temperature: Optional temperature override
            max_tokens: Optional max tokens override

        Returns:
            CompletionResponse with the model's response
        """
        pass

    @abstractmethod
    async def stream(
        self,
        messages: list[Message],
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> AsyncIterator[str]:
        """
        Stream a completion for the given messages.

        Args:
            messages: List of conversation messages
            system_prompt: Optional system prompt
            temperature: Optional temperature override
            max_tokens: Optional max tokens override

        Yields:
            String chunks of the response
        """
        pass

    def supports_vision(self) -> bool:
        """Check if this provider supports vision/image input."""
        return self.config.supports_vision

    def supports_streaming(self) -> bool:
        """Check if this provider supports streaming."""
        return self.config.supports_streaming

    def supports_function_calling(self) -> bool:
        """Check if this provider supports function calling."""
        return self.config.supports_function_calling

    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Estimate the cost for a request."""
        total_tokens = input_tokens + output_tokens
        return (total_tokens / 1000) * self.config.cost_per_1k_tokens

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(model={self.config.model_id})"
