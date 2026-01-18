"""
WejdanAI Claude Provider
=========================
Provider for Anthropic's Claude - the orchestrator and analyzer.
"""

import json
import time
from typing import AsyncIterator, Optional

from ..config.models import MODELS, ModelProvider
from .base import BaseProvider, CompletionResponse, Message


class ClaudeProvider(BaseProvider):
    """Provider for Anthropic's Claude models."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_id: Optional[str] = None,
        **kwargs,
    ):
        config = MODELS[ModelProvider.CLAUDE]
        if model_id:
            config.model_id = model_id
        super().__init__(config, api_key, **kwargs)

    def _get_headers(self) -> dict[str, str]:
        headers = super()._get_headers()
        if self.api_key:
            headers["x-api-key"] = self.api_key
            headers["anthropic-version"] = "2023-06-01"
        return headers

    def _format_messages(
        self,
        messages: list[Message],
    ) -> list[dict]:
        """Format messages for Claude API."""
        formatted = []

        for msg in messages:
            if msg.images:
                # Multimodal message
                content = []

                for img in msg.images:
                    if img.startswith("http"):
                        content.append({
                            "type": "image",
                            "source": {
                                "type": "url",
                                "url": img,
                            },
                        })
                    else:
                        # Base64
                        content.append({
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": img,
                            },
                        })

                content.append({
                    "type": "text",
                    "text": msg.content,
                })

                formatted.append({"role": msg.role, "content": content})
            else:
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
        """Generate a completion using Claude."""
        await self._rate_limit()
        start_time = time.time()

        # Default orchestrator system prompt
        if not system_prompt:
            system_prompt = (
                "You are Claude, an AI assistant by Anthropic. You excel at "
                "complex reasoning, document analysis, and orchestrating tasks. "
                "Provide thorough, well-structured responses."
            )

        try:
            formatted_messages = self._format_messages(messages)

            payload = {
                "model": self.config.model_id,
                "messages": formatted_messages,
                "system": system_prompt,
                "temperature": temperature or self.config.temperature,
                "max_tokens": max_tokens or 4096,
            }

            response = await self._retry_with_backoff(
                self.client.post,
                f"{self.config.api_base}/messages",
                json=payload,
            )
            response.raise_for_status()

            data = response.json()
            latency = (time.time() - start_time) * 1000

            # Extract content from Claude response
            content = ""
            for block in data.get("content", []):
                if block.get("type") == "text":
                    content += block.get("text", "")

            usage = data.get("usage", {})

            return CompletionResponse(
                content=content,
                model=data.get("model", self.config.model_id),
                provider=ModelProvider.CLAUDE,
                usage={
                    "input_tokens": usage.get("input_tokens", 0),
                    "output_tokens": usage.get("output_tokens", 0),
                },
                latency_ms=latency,
                success=True,
            )

        except Exception as e:
            return CompletionResponse(
                content="",
                model=self.config.model_id,
                provider=ModelProvider.CLAUDE,
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
        """Stream a completion using Claude."""
        await self._rate_limit()

        if not system_prompt:
            system_prompt = (
                "You are Claude, an AI assistant by Anthropic. "
                "You excel at complex reasoning and analysis."
            )

        formatted_messages = self._format_messages(messages)

        payload = {
            "model": self.config.model_id,
            "messages": formatted_messages,
            "system": system_prompt,
            "temperature": temperature or self.config.temperature,
            "max_tokens": max_tokens or 4096,
            "stream": True,
        }

        async with self.client.stream(
            "POST",
            f"{self.config.api_base}/messages",
            json=payload,
        ) as response:
            response.raise_for_status()

            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data_str = line[6:]
                    try:
                        data = json.loads(data_str)
                        if data.get("type") == "content_block_delta":
                            delta = data.get("delta", {})
                            if text := delta.get("text"):
                                yield text
                    except json.JSONDecodeError:
                        continue
