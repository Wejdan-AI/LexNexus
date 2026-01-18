"""
WejdanAI Perplexity Provider
=============================
Provider for Perplexity's research-focused models with citations.
"""

import json
import time
from typing import AsyncIterator, Optional

from ..config.models import MODELS, ModelProvider
from .base import BaseProvider, CompletionResponse, Message


class PerplexityProvider(BaseProvider):
    """Provider for Perplexity's research models with web search."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_id: Optional[str] = None,
        **kwargs,
    ):
        config = MODELS[ModelProvider.PERPLEXITY]
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
        """Format messages for Perplexity API."""
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
        search_domain_filter: Optional[list[str]] = None,
        return_citations: bool = True,
    ) -> CompletionResponse:
        """Generate a completion using Perplexity with web search."""
        await self._rate_limit()
        start_time = time.time()

        # Add research-focused system prompt
        if not system_prompt:
            system_prompt = (
                "You are a research assistant that provides accurate, "
                "well-sourced information. Always cite your sources and "
                "indicate when information may be outdated or uncertain."
            )

        try:
            formatted_messages = self._format_messages(messages, system_prompt)

            payload = {
                "model": self.config.model_id,
                "messages": formatted_messages,
                "temperature": temperature or 0.2,  # Lower for accuracy
                "max_tokens": max_tokens or self.config.max_tokens,
                "return_citations": return_citations,
            }

            if search_domain_filter:
                payload["search_domain_filter"] = search_domain_filter

            response = await self._retry_with_backoff(
                self.client.post,
                f"{self.config.api_base}/chat/completions",
                json=payload,
            )
            response.raise_for_status()

            data = response.json()
            latency = (time.time() - start_time) * 1000

            # Extract citations from Perplexity response
            citations = data.get("citations", [])

            return CompletionResponse(
                content=data["choices"][0]["message"]["content"],
                model=data.get("model", self.config.model_id),
                provider=ModelProvider.PERPLEXITY,
                usage={
                    "input_tokens": data.get("usage", {}).get("prompt_tokens", 0),
                    "output_tokens": data.get("usage", {}).get("completion_tokens", 0),
                },
                latency_ms=latency,
                citations=citations,
                success=True,
            )

        except Exception as e:
            return CompletionResponse(
                content="",
                model=self.config.model_id,
                provider=ModelProvider.PERPLEXITY,
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
        """Stream a completion using Perplexity."""
        await self._rate_limit()

        if not system_prompt:
            system_prompt = (
                "You are a research assistant that provides accurate, "
                "well-sourced information."
            )

        formatted_messages = self._format_messages(messages, system_prompt)

        payload = {
            "model": self.config.model_id,
            "messages": formatted_messages,
            "temperature": temperature or 0.2,
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
