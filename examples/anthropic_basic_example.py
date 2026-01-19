"""
Basic Anthropic API Example
Demonstrates simple usage of the Anthropic service for text generation.
"""

import sys
import os

# Add parent directory to path to import the service
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.anthropic_service import AnthropicService


def main():
    print("=== Anthropic API Basic Example ===\n")

    # Initialize the service
    # API key will be loaded from ANTHROPIC_API_KEY environment variable
    service = AnthropicService()

    # Example 1: Simple completion
    print("Example 1: Simple Completion")
    print("-" * 50)
    prompt = "Explain what a REST API is in 2-3 sentences."
    response = service.simple_completion(prompt, max_tokens=1024)
    print(f"Prompt: {prompt}")
    print(f"Response: {response}\n")

    # Example 2: Chat completion with conversation history
    print("\nExample 2: Chat Completion")
    print("-" * 50)
    messages = [
        {"role": "user", "content": "What is Python?"},
        {"role": "assistant", "content": "Python is a high-level, interpreted programming language known for its simplicity and readability."},
        {"role": "user", "content": "What are its main uses?"}
    ]

    result = service.chat_completion(messages, max_tokens=1024)
    print(f"Response: {result['text']}")
    print(f"Tokens used - Input: {result['usage']['input_tokens']}, Output: {result['usage']['output_tokens']}\n")

    # Example 3: Using system prompts
    print("\nExample 3: System Prompt")
    print("-" * 50)
    system_prompt = "You are a helpful assistant that responds in a pirate accent."
    messages = [
        {"role": "user", "content": "Tell me about cloud computing."}
    ]

    result = service.chat_completion(
        messages,
        system=system_prompt,
        max_tokens=1024
    )
    print(f"Response: {result['text']}\n")


if __name__ == "__main__":
    main()
