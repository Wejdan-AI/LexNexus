"""
Anthropic Streaming Example
Demonstrates real-time streaming of responses from Claude.
"""

import sys
import os

# Add parent directory to path to import the service
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.anthropic_service import AnthropicService


def main():
    print("=== Anthropic Streaming Example ===\n")

    # Initialize the service
    service = AnthropicService()

    # Example: Stream a creative writing response
    print("Example: Streaming Creative Writing")
    print("-" * 60)
    prompt = "Write a short story about a robot learning to paint. Keep it under 200 words."

    print(f"Prompt: {prompt}\n")
    print("Streaming response:")
    print("-" * 60)

    # Stream the response
    for chunk in service.stream_completion(prompt, max_tokens=2048):
        print(chunk, end='', flush=True)

    print("\n" + "-" * 60)
    print("\nStreaming complete!")


if __name__ == "__main__":
    main()
