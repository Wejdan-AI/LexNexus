"""
WejdanAI Qwen Provider
=======================
Provider for Alibaba's Qwen models - optimized for Arabic/Chinese.
"""

import json
import time
from typing import AsyncIterator, Optional

from ..config.models import MODELS, ModelProvider
from .base import BaseProvider, CompletionResponse, Message


class QwenProvider(BaseProvider):
    """Provider for Qwen models - multilingual specialist."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_id: Optional[str] = None,
        **kwargs,
    ):
        config = MODELS[ModelProvider.QWEN]
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
    ) -> dict:
        """Format messages for Qwen/DashScope API."""
        formatted_messages = []

        if system_prompt:
            formatted_messages.append({
                "role": "system",
                "content": system_prompt,
            })

        for msg in messages:
            content = []

            # Add text content
            if msg.content:
                content.append({"text": msg.content})

            # Add images for vision
            for img in msg.images:
                if img.startswith("http"):
                    content.append({"image": img})
                else:
                    # Base64
                    content.append({
                        "image": f"data:image/png;base64,{img}"
                    })

            if len(content) == 1 and "text" in content[0]:
                # Simple text message
                formatted_messages.append({
                    "role": msg.role,
                    "content": content[0]["text"],
                })
            else:
                # Multimodal message
                formatted_messages.append({
                    "role": msg.role,
                    "content": content,
                })

        return {"messages": formatted_messages}

    async def complete(
        self,
        messages: list[Message],
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> CompletionResponse:
        """Generate a completion using Qwen."""
        await self._rate_limit()
        start_time = time.time()

        # Multilingual system prompt
        if not system_prompt:
            system_prompt = (
                "أنت مساعد ذكي متعدد اللغات. تتحدث العربية والصينية والإنجليزية بطلاقة. "
                "You are a multilingual AI assistant fluent in Arabic, Chinese, and English. "
                "你是一个精通阿拉伯语、中文和英语的多语言人工智能助手。"
            )

        try:
            payload = self._format_messages(messages, system_prompt)
            payload["model"] = self.config.model_id
            payload["input"] = payload.pop("messages")
            payload["parameters"] = {
                "temperature": temperature or self.config.temperature,
                "max_tokens": max_tokens or self.config.max_tokens,
                "result_format": "message",
            }

            response = await self._retry_with_backoff(
                self.client.post,
                f"{self.config.api_base}/services/aigc/text-generation/generation",
                json=payload,
            )
            response.raise_for_status()

            data = response.json()
            latency = (time.time() - start_time) * 1000

            # Extract content from Qwen response
            output = data.get("output", {})
            content = output.get("choices", [{}])[0].get("message", {}).get("content", "")
            if not content:
                content = output.get("text", "")

            usage = data.get("usage", {})

            return CompletionResponse(
                content=content,
                model=self.config.model_id,
                provider=ModelProvider.QWEN,
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
                provider=ModelProvider.QWEN,
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
        """Stream a completion using Qwen."""
        await self._rate_limit()

        if not system_prompt:
            system_prompt = (
                "أنت مساعد ذكي متعدد اللغات. "
                "You are a multilingual AI assistant."
            )

        payload = self._format_messages(messages, system_prompt)
        payload["model"] = self.config.model_id
        payload["input"] = payload.pop("messages")
        payload["parameters"] = {
            "temperature": temperature or self.config.temperature,
            "max_tokens": max_tokens or self.config.max_tokens,
            "result_format": "message",
            "incremental_output": True,
        }

        async with self.client.stream(
            "POST",
            f"{self.config.api_base}/services/aigc/text-generation/generation",
            json=payload,
        ) as response:
            response.raise_for_status()

            async for line in response.aiter_lines():
                if line.startswith("data:"):
                    data_str = line[5:].strip()
                    if not data_str:
                        continue
                    try:
                        data = json.loads(data_str)
                        output = data.get("output", {})
                        text = output.get("text", "")
                        if text:
                            yield text
                    except json.JSONDecodeError:
                        continue
