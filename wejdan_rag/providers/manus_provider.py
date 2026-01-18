"""
WejdanAI Manus Provider
========================
Provider for Manus AI - autonomous agents and web automation.
"""

import json
import time
from typing import Any, AsyncIterator, Optional

from ..config.models import MODELS, ModelProvider
from .base import BaseProvider, CompletionResponse, Message


class ManusProvider(BaseProvider):
    """Provider for Manus AI - autonomous multi-step tasks."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_id: Optional[str] = None,
        **kwargs,
    ):
        config = MODELS[ModelProvider.MANUS]
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
        """Format messages for Manus API."""
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
        tools: Optional[list[dict]] = None,
        autonomous: bool = False,
    ) -> CompletionResponse:
        """Generate a completion using Manus AI."""
        await self._rate_limit()
        start_time = time.time()

        # Autonomous agent system prompt
        if not system_prompt:
            system_prompt = (
                "You are Manus, an autonomous AI agent capable of executing "
                "multi-step tasks. You can browse the web, interact with APIs, "
                "and complete complex workflows. Plan and execute tasks step by step."
            )

        try:
            formatted_messages = self._format_messages(messages, system_prompt)

            payload = {
                "model": self.config.model_id,
                "messages": formatted_messages,
                "temperature": temperature or self.config.temperature,
                "max_tokens": max_tokens or self.config.max_tokens,
            }

            if tools:
                payload["tools"] = tools

            if autonomous:
                payload["autonomous_mode"] = True
                payload["max_steps"] = 10

            response = await self._retry_with_backoff(
                self.client.post,
                f"{self.config.api_base}/chat/completions",
                json=payload,
            )
            response.raise_for_status()

            data = response.json()
            latency = (time.time() - start_time) * 1000

            # Extract execution steps if available
            execution_steps = data.get("execution_steps", [])

            return CompletionResponse(
                content=data["choices"][0]["message"]["content"],
                model=data.get("model", self.config.model_id),
                provider=ModelProvider.MANUS,
                usage={
                    "input_tokens": data.get("usage", {}).get("prompt_tokens", 0),
                    "output_tokens": data.get("usage", {}).get("completion_tokens", 0),
                },
                latency_ms=latency,
                metadata={
                    "autonomous": autonomous,
                    "execution_steps": execution_steps,
                },
                success=True,
            )

        except Exception as e:
            return CompletionResponse(
                content="",
                model=self.config.model_id,
                provider=ModelProvider.MANUS,
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
        """Stream a completion using Manus AI."""
        await self._rate_limit()

        if not system_prompt:
            system_prompt = (
                "You are Manus, an autonomous AI agent for multi-step tasks."
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

    async def execute_task(
        self,
        task: str,
        context: Optional[dict[str, Any]] = None,
        max_steps: int = 10,
    ) -> CompletionResponse:
        """
        Execute an autonomous multi-step task.

        Args:
            task: Description of the task to execute
            context: Optional context/data for the task
            max_steps: Maximum number of steps to execute

        Returns:
            CompletionResponse with task results
        """
        messages = [Message(role="user", content=task)]

        system_prompt = (
            f"Execute the following task autonomously. "
            f"Context: {json.dumps(context) if context else 'None'}. "
            f"Maximum steps: {max_steps}. "
            f"Report your progress and final results."
        )

        return await self.complete(
            messages=messages,
            system_prompt=system_prompt,
            autonomous=True,
        )
