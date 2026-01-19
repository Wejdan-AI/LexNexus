"""
Anthropic Extended Thinking Example
Demonstrates the use of extended thinking feature for complex reasoning tasks.
"""

import sys
import os

# Add parent directory to path to import the service
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.anthropic_service import AnthropicService


def main():
    print("=== Anthropic Extended Thinking Example ===\n")

    # Initialize the service
    service = AnthropicService()

    # Example 1: Complex problem solving with thinking
    print("Example 1: Problem Solving with Extended Thinking")
    print("-" * 60)
    prompt = """
    I have a 3-gallon jug and a 5-gallon jug. I need to measure exactly 4 gallons of water.
    How can I do this? Explain your reasoning step by step.
    """

    response = service.simple_completion(
        prompt,
        max_tokens=4096,
        enable_thinking=True,
        thinking_budget=16000
    )

    print(f"Prompt: {prompt.strip()}")
    print(f"\nResponse:\n{response}\n")

    # Example 2: Advanced API usage with thinking configuration
    print("\nExample 2: Direct API Call with Thinking Config")
    print("-" * 60)

    messages = [
        {
            "role": "user",
            "content": "Design a scalable architecture for a real-time chat application with 1 million concurrent users."
        }
    ]

    thinking_config = {
        "type": "enabled",
        "budget_tokens": 16000
    }

    message = service.create_message(
        messages=messages,
        model="claude-sonnet-4-5-20250929",
        max_tokens=8192,
        temperature=1,
        thinking=thinking_config
    )

    print("Full response object:")
    print(f"Model: {message.model}")
    print(f"Stop reason: {message.stop_reason}")
    print(f"Usage: {message.usage}")
    print(f"\nContent blocks:")
    for i, block in enumerate(message.content):
        print(f"\nBlock {i + 1} (type: {block.type}):")
        if block.type == "thinking":
            print(f"Thinking: {block.thinking[:200]}...")  # Show first 200 chars
        elif block.type == "text":
            print(f"Text: {block.text}")


if __name__ == "__main__":
    main()
