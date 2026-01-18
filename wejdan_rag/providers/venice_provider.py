"""
WejdanAI Venice Provider
=========================
Provider for Venice AI - privacy-focused, uncensored models.
"""

import json
import time
from typing import AsyncIterator, Optional

from ..config.models import MODELS, ModelProvider
from .base import BaseProvider, CompletionResponse, Message


class VeniceProvider(BaseProvider):
    """Provider for Venice AI - privacy-first models."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_id: Optional[str] = None,
        **kwargs,
    ):
        config = MODELS[ModelProvider.VENICE]
        if model_id:
            config.model_id = model_id
        super().__init__(config, api_key, **kwargs)

    def _get_headers(self) -> dict[str, str]:
        headers = super()._get_headers()
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _format_messages(
        self,
        messages: list[Message],
        system_prompt: Optional[str] = None,
    ) -> list[dict]:
        """Format messages for Venice API (OpenAI compatible)."""
        formatted = []

        if system_prompt:
            formatted.append({
                "role": "system",
                "content": system_prompt,
            })

        for msg in messages:
            formatted.append({
                "role": msg.role,
                "content": msg.content,
            })

        return formatted

    async def complete(
        self,
        messages: list[Message],
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> CompletionResponse:
        """Generate a completion using Venice AI."""
        await self._rate_limit()
        start_time = time.time()

        # Privacy-focused system prompt
        if not system_prompt:
            system_prompt = (
                "You are a helpful AI assistant. Your responses are private "
                "and not logged or monitored. Provide direct, honest answers."
            )

        try:
            formatted_messages = self._format_messages(messages, system_prompt)

            payload = {
                "model": self.config.model_id,
                "messages": formatted_messages,
                "temperature": temperature or self.config.temperature,
                "max_tokens": max_tokens or self.config.max_tokens,
            }

            response = await self._retry_with_backoff(
                self.client.post,
                f"{self.config.api_base}/chat/completions",
                json=payload,
            )
            response.raise_for_status()

            data = response.json()
            latency = (time.time() - start_time) * 1000

            return CompletionResponse(
                content=data["choices"][0]["message"]["content"],
                model=data.get("model", self.config.model_id),
                provider=ModelProvider.VENICE,
                usage={
                    "input_tokens": data.get("usage", {}).get("prompt_tokens", 0),
                    "output_tokens": data.get("usage", {}).get("completion_tokens", 0),
                },
                latency_ms=latency,
                metadata={"privacy_mode": True},
                success=True,
            )

        except Exception as e:
            return CompletionResponse(
                content="",
                model=self.config.model_id,
                provider=ModelProvider.VENICE,
                latency_ms=(time.time() - start_time) * 1000,
                error=str(e),
                success=False,
            )

    async def stream(
        self,
        messages: list[Message],
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> AsyncIterator[str]:
        """Stream a completion using Venice AI."""
        await self._rate_limit()

        if not system_prompt:
            system_prompt = (
                "You are a helpful AI assistant. Your responses are private."
            )

        formatted_messages = self._format_messages(messages, system_prompt)

        payload = {
            "model": self.config.model_id,
            "messages": formatted_messages,
            "temperature": temperature or self.config.temperature,
            "max_tokens": max_tokens or self.config.max_tokens,
            "stream": True,
        }

        async with self.client.stream(
            "POST",
            f"{self.config.api_base}/chat/completions",
            json=payload,
        ) as response:
            response.raise_for_status()

            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data)
                        delta = chunk["choices"][0].get("delta", {})
                        if content := delta.get("content"):
                            yield content
                    except json.JSONDecodeError:
                        continue
