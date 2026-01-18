"""
WejdanAI Copilot Provider
==========================
Provider for Microsoft Copilot - enterprise and Office integration.
"""

import json
import time
from typing import AsyncIterator, Optional

from ..config.models import MODELS, ModelProvider
from .base import BaseProvider, CompletionResponse, Message


class CopilotProvider(BaseProvider):
    """Provider for Microsoft Copilot - enterprise workflows."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_id: Optional[str] = None,
        azure_endpoint: Optional[str] = None,
        **kwargs,
    ):
        config = MODELS[ModelProvider.COPILOT]
        if model_id:
            config.model_id = model_id
        if azure_endpoint:
            config.api_base = azure_endpoint
        super().__init__(config, api_key, **kwargs)
        self.azure_endpoint = azure_endpoint

    def _get_headers(self) -> dict[str, str]:
        headers = super()._get_headers()
        if self.api_key:
            headers["api-key"] = self.api_key
        return headers

    def _format_messages(
        self,
        messages: list[Message],
        system_prompt: Optional[str] = None,
    ) -> list[dict]:
        """Format messages for Azure OpenAI/Copilot API."""
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
        """Generate a completion using Microsoft Copilot."""
        await self._rate_limit()
        start_time = time.time()

        # Enterprise-focused system prompt
        if not system_prompt:
            system_prompt = (
                "You are Microsoft Copilot, an AI assistant integrated with "
                "Microsoft 365. You help with Office documents, enterprise "
                "workflows, and business productivity tasks."
            )

        try:
            formatted_messages = self._format_messages(messages, system_prompt)

            payload = {
                "messages": formatted_messages,
                "temperature": temperature or self.config.temperature,
                "max_tokens": max_tokens or self.config.max_tokens,
            }

            # Azure OpenAI endpoint format
            api_url = f"{self.config.api_base}/openai/deployments/{self.config.model_id}/chat/completions?api-version=2024-02-01"

            response = await self._retry_with_backoff(
                self.client.post,
                api_url,
                json=payload,
            )
            response.raise_for_status()

            data = response.json()
            latency = (time.time() - start_time) * 1000

            return CompletionResponse(
                content=data["choices"][0]["message"]["content"],
                model=data.get("model", self.config.model_id),
                provider=ModelProvider.COPILOT,
                usage={
                    "input_tokens": data.get("usage", {}).get("prompt_tokens", 0),
                    "output_tokens": data.get("usage", {}).get("completion_tokens", 0),
                },
                latency_ms=latency,
                metadata={"enterprise_mode": True},
                success=True,
            )

        except Exception as e:
            return CompletionResponse(
                content="",
                model=self.config.model_id,
                provider=ModelProvider.COPILOT,
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
        """Stream a completion using Microsoft Copilot."""
        await self._rate_limit()

        if not system_prompt:
            system_prompt = (
                "You are Microsoft Copilot, helping with Office and enterprise tasks."
            )

        formatted_messages = self._format_messages(messages, system_prompt)

        payload = {
            "messages": formatted_messages,
            "temperature": temperature or self.config.temperature,
            "max_tokens": max_tokens or self.config.max_tokens,
            "stream": True,
        }

        api_url = f"{self.config.api_base}/openai/deployments/{self.config.model_id}/chat/completions?api-version=2024-02-01"

        async with self.client.stream(
            "POST",
            api_url,
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
