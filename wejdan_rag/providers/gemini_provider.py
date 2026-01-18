"""
WejdanAI Google Gemini Provider
================================
Provider for Google's Gemini models.
"""

import json
import time
from typing import AsyncIterator, Optional

from ..config.models import MODELS, ModelProvider
from .base import BaseProvider, CompletionResponse, Message


class GeminiProvider(BaseProvider):
    """Provider for Google's Gemini models."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_id: Optional[str] = None,
        **kwargs,
    ):
        config = MODELS[ModelProvider.GEMINI]
        if model_id:
            config.model_id = model_id
        super().__init__(config, api_key, **kwargs)

    def _get_api_url(self, stream: bool = False) -> str:
        """Get the API URL for Gemini."""
        action = "streamGenerateContent" if stream else "generateContent"
        return (
            f"{self.config.api_base}/models/{self.config.model_id}:{action}"
            f"?key={self.api_key}"
        )

    def _format_messages(
        self,
        messages: list[Message],
        system_prompt: Optional[str] = None,
    ) -> dict:
        """Format messages for Gemini API."""
        contents = []

        for msg in messages:
            parts = []

            # Add text content
            if msg.content:
                parts.append({"text": msg.content})

            # Add images
            for img in msg.images:
                if img.startswith("http"):
                    parts.append({
                        "file_data": {
                            "mime_type": "image/png",
                            "file_uri": img,
                        }
                    })
                else:
                    # Base64
                    parts.append({
                        "inline_data": {
                            "mime_type": "image/png",
                            "data": img,
                        }
                    })

            role = "user" if msg.role == "user" else "model"
            contents.append({"role": role, "parts": parts})

        payload = {"contents": contents}

        if system_prompt:
            payload["system_instruction"] = {
                "parts": [{"text": system_prompt}]
            }

        return payload

    async def complete(
        self,
        messages: list[Message],
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> CompletionResponse:
        """Generate a completion using Gemini."""
        await self._rate_limit()
        start_time = time.time()

        try:
            payload = self._format_messages(messages, system_prompt)
            payload["generationConfig"] = {
                "temperature": temperature or self.config.temperature,
                "maxOutputTokens": max_tokens or self.config.max_tokens,
            }

            response = await self._retry_with_backoff(
                self.client.post,
                self._get_api_url(),
                json=payload,
            )
            response.raise_for_status()

            data = response.json()
            latency = (time.time() - start_time) * 1000

            # Extract content from Gemini response
            content = ""
            if "candidates" in data and data["candidates"]:
                parts = data["candidates"][0].get("content", {}).get("parts", [])
                content = "".join(p.get("text", "") for p in parts)

            # Extract usage
            usage_metadata = data.get("usageMetadata", {})

            return CompletionResponse(
                content=content,
                model=self.config.model_id,
                provider=ModelProvider.GEMINI,
                usage={
                    "input_tokens": usage_metadata.get("promptTokenCount", 0),
                    "output_tokens": usage_metadata.get("candidatesTokenCount", 0),
                },
                latency_ms=latency,
                success=True,
            )

        except Exception as e:
            return CompletionResponse(
                content="",
                model=self.config.model_id,
                provider=ModelProvider.GEMINI,
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
        """Stream a completion using Gemini."""
        await self._rate_limit()

        payload = self._format_messages(messages, system_prompt)
        payload["generationConfig"] = {
            "temperature": temperature or self.config.temperature,
            "maxOutputTokens": max_tokens or self.config.max_tokens,
        }

        async with self.client.stream(
            "POST",
            self._get_api_url(stream=True),
            json=payload,
        ) as response:
            response.raise_for_status()

            async for line in response.aiter_lines():
                if not line:
                    continue
                try:
                    # Gemini streams JSON objects
                    if line.startswith("["):
                        line = line[1:]
                    if line.startswith(","):
                        line = line[1:]
                    if line.endswith("]"):
                        line = line[:-1]

                    data = json.loads(line)
                    if "candidates" in data:
                        parts = data["candidates"][0].get("content", {}).get("parts", [])
                        for part in parts:
                            if text := part.get("text"):
                                yield text
                except json.JSONDecodeError:
                    continue
