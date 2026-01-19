"""
Direct Anthropic SDK Example
Demonstrates direct usage of the Anthropic SDK (similar to the user's original code).
This shows how to use the SDK without the service wrapper.
"""

import os
import anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def main():
    print("=== Direct Anthropic SDK Usage ===\n")

    # Initialize the client
    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )

    # Example 1: Basic message creation
    print("Example 1: Basic Message")
    print("-" * 60)

    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "What is machine learning?"
            }
        ]
    )

    print(f"Response: {message.content[0].text}\n")

    # Example 2: Extended thinking enabled
    print("\nExample 2: With Extended Thinking")
    print("-" * 60)

    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=20000,
        temperature=1,
        messages=[
            {
                "role": "user",
                "content": "Solve this logic puzzle: A farmer needs to cross a river with a fox, a chicken, and a bag of grain. The boat can only carry the farmer and one item. If left alone, the fox will eat the chicken, and the chicken will eat the grain. How does the farmer get everything across safely?"
            }
        ],
        thinking={
            "type": "enabled",
            "budget_tokens": 16000
        }
    )

    print("Content blocks in response:")
    for i, block in enumerate(message.content):
        print(f"\nBlock {i + 1} - Type: {block.type}")
        if block.type == "thinking":
            print(f"Thinking content: {block.thinking[:200]}...")
        elif block.type == "text":
            print(f"Text content: {block.text}")

    # Example 3: Multi-turn conversation
    print("\n\nExample 3: Multi-turn Conversation")
    print("-" * 60)

    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2048,
        temperature=1,
        messages=[
            {
                "role": "user",
                "content": "What is Python used for?"
            },
            {
                "role": "assistant",
                "content": "Python is used for web development, data science, machine learning, automation, and more."
            },
            {
                "role": "user",
                "content": "Which frameworks are popular for web development?"
            }
        ]
    )

    print(f"Response: {message.content[0].text}\n")

    # Example 4: Using system prompts
    print("\nExample 4: With System Prompt")
    print("-" * 60)

    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        system="You are a helpful coding assistant specialized in Python. Provide concise, practical answers.",
        messages=[
            {
                "role": "user",
                "content": "How do I read a CSV file in Python?"
            }
        ]
    )

    print(f"Response: {message.content[0].text}\n")


if __name__ == "__main__":
    main()
