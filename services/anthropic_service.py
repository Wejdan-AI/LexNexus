"""
Anthropic Claude API Service
Provides a clean interface for interacting with Claude models using the official SDK.
"""

import os
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
import anthropic

# Load environment variables
load_dotenv()


class AnthropicService:
    """Service class for interacting with Anthropic's Claude API."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Anthropic service.

        Args:
            api_key: Optional API key. If not provided, will use ANTHROPIC_API_KEY env var.
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Anthropic API key not found. Set ANTHROPIC_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self.client = anthropic.Anthropic(api_key=self.api_key)

    def create_message(
        self,
        messages: List[Dict[str, Any]],
        model: str = "claude-sonnet-4-5-20250929",
        max_tokens: int = 20000,
        temperature: float = 1.0,
        system: Optional[str] = None,
        thinking: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> anthropic.types.Message:
        """
        Create a message using Claude.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model identifier (default: claude-sonnet-4-5-20250929)
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0-1)
            system: Optional system prompt
            thinking: Optional thinking configuration
                     Example: {"type": "enabled", "budget_tokens": 16000}
            **kwargs: Additional parameters to pass to the API

        Returns:
            Message object from the API
        """
        params = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages,
        }

        if system:
            params["system"] = system

        if thinking:
            params["thinking"] = thinking

        # Add any additional parameters
        params.update(kwargs)

        return self.client.messages.create(**params)

    def simple_completion(
        self,
        prompt: str,
        model: str = "claude-sonnet-4-5-20250929",
        max_tokens: int = 4096,
        temperature: float = 1.0,
        enable_thinking: bool = False,
        thinking_budget: int = 16000
    ) -> str:
        """
        Simple completion interface - send a prompt and get a text response.

        Args:
            prompt: The prompt text
            model: Model identifier
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            enable_thinking: Whether to enable extended thinking
            thinking_budget: Token budget for thinking (if enabled)

        Returns:
            The generated text response
        """
        messages = [{"role": "user", "content": prompt}]

        thinking_config = None
        if enable_thinking:
            thinking_config = {
                "type": "enabled",
                "budget_tokens": thinking_budget
            }

        response = self.create_message(
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            thinking=thinking_config
        )

        # Extract text from response
        text_content = []
        for block in response.content:
            if block.type == "text":
                text_content.append(block.text)

        return "\n".join(text_content)

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "claude-sonnet-4-5-20250929",
        max_tokens: int = 8192,
        temperature: float = 1.0,
        system: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Chat completion interface - maintains conversation history.

        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model identifier
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            system: Optional system prompt

        Returns:
            Dictionary with response details including text, usage stats, etc.
        """
        response = self.create_message(
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system
        )

        # Extract text content
        text_content = []
        for block in response.content:
            if block.type == "text":
                text_content.append(block.text)

        return {
            "text": "\n".join(text_content),
            "model": response.model,
            "stop_reason": response.stop_reason,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens
            },
            "raw_response": response
        }

    def stream_completion(
        self,
        prompt: str,
        model: str = "claude-sonnet-4-5-20250929",
        max_tokens: int = 4096,
        temperature: float = 1.0
    ):
        """
        Stream a completion response.

        Args:
            prompt: The prompt text
            model: Model identifier
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature

        Yields:
            Text chunks as they are generated
        """
        messages = [{"role": "user", "content": prompt}]

        with self.client.messages.stream(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=messages
        ) as stream:
            for text in stream.text_stream:
                yield text


# Convenience function for quick usage
def quick_completion(prompt: str, api_key: Optional[str] = None) -> str:
    """
    Quick completion function for simple use cases.

    Args:
        prompt: The prompt text
        api_key: Optional API key

    Returns:
        The generated text response
    """
    service = AnthropicService(api_key=api_key)
    return service.simple_completion(prompt)
