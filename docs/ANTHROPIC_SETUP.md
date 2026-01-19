# Anthropic API Setup Guide

This guide explains how to set up and use the Anthropic Claude API in the WejdanAI project.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Using the Service Wrapper](#using-the-service-wrapper)
  - [Direct SDK Usage](#direct-sdk-usage)
  - [LLM Orchestrator Integration](#llm-orchestrator-integration)
- [Examples](#examples)
- [Advanced Features](#advanced-features)
  - [Extended Thinking](#extended-thinking)
  - [Streaming Responses](#streaming-responses)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- Python 3.8 or higher
- An Anthropic API key (get one at https://console.anthropic.com/)

## Installation

1. Install the required Python packages:

```bash
pip install -r requirements.txt
```

This will install:
- `anthropic` - Official Anthropic SDK
- `fastapi` - For the LLM orchestrator
- `uvicorn` - ASGI server
- `httpx` - Async HTTP client
- `python-dotenv` - Environment variable management
- Other AI provider SDKs (OpenAI, Google Generative AI)

## Configuration

### Setting up Environment Variables

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Edit `.env` and add your Anthropic API key:

```env
ANTHROPIC_API_KEY=your_actual_api_key_here
```

**Important**: Never commit your `.env` file to version control. It's already included in `.gitignore`.

### Vercel/Production Deployment

For production deployments on Vercel or other platforms:

1. Add `ANTHROPIC_API_KEY` to your environment variables in the Vercel dashboard
2. The application will automatically use it at runtime

## Usage

### Using the Service Wrapper

The `AnthropicService` class provides a clean, easy-to-use interface:

```python
from services.anthropic_service import AnthropicService

# Initialize the service
service = AnthropicService()

# Simple completion
response = service.simple_completion("What is machine learning?")
print(response)

# Chat completion with conversation history
messages = [
    {"role": "user", "content": "What is Python?"},
    {"role": "assistant", "content": "Python is a programming language."},
    {"role": "user", "content": "What are its main uses?"}
]

result = service.chat_completion(messages)
print(result['text'])
print(f"Tokens used: {result['usage']}")
```

### Direct SDK Usage

For more control, you can use the Anthropic SDK directly:

```python
import anthropic
import os

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude!"}
    ]
)

print(message.content[0].text)
```

### LLM Orchestrator Integration

The FastAPI-based LLM orchestrator supports Anthropic with automatic fallback:

1. Start the orchestrator:

```bash
python LLM
```

2. Configure the Anthropic connection via the API:

```python
import httpx

# Save Anthropic connection
response = httpx.post("http://localhost:8000/api/connections", json={
    "anthropic": {
        "provider": "anthropic",
        "enabled": True,
        "api_key": "your_api_key",
        "default_model": "claude-sonnet-4-5-20250929",
        "use_sdk": True  # Use official SDK instead of OpenAI-compatible endpoint
    }
})
```

3. Make a request:

```python
response = httpx.post("http://localhost:8000/api/run", json={
    "workflow_id": "default",
    "task": "general_query",
    "query": "Explain quantum computing",
    "preference": "quality",  # Routes to Anthropic first
    "context": {
        "enable_thinking": False  # Set to True for extended thinking
    }
})

result = response.json()
print(result['answer'])
print(f"Provider: {result['provider']}")
print(f"Latency: {result['latency_ms']}ms")
```

## Examples

We provide several example scripts in the `examples/` directory:

### Basic Example

```bash
python examples/anthropic_basic_example.py
```

Demonstrates:
- Simple completions
- Chat completions
- System prompts

### Extended Thinking Example

```bash
python examples/anthropic_thinking_example.py
```

Demonstrates:
- Complex problem solving with extended thinking
- Direct access to thinking content blocks

### Streaming Example

```bash
python examples/anthropic_streaming_example.py
```

Demonstrates:
- Real-time streaming of responses

### Direct SDK Example

```bash
python examples/anthropic_direct_sdk_example.py
```

Demonstrates:
- Direct SDK usage without wrappers
- Multi-turn conversations
- System prompts

## Advanced Features

### Extended Thinking

Extended thinking allows Claude to show its reasoning process:

```python
service = AnthropicService()

# Enable thinking with a token budget
response = service.simple_completion(
    "Solve this complex logic puzzle...",
    enable_thinking=True,
    thinking_budget=16000  # Allocate tokens for thinking
)
```

When using the SDK directly:

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=20000,
    messages=[{"role": "user", "content": "Complex problem here..."}],
    thinking={
        "type": "enabled",
        "budget_tokens": 16000
    }
)

# Access thinking blocks
for block in message.content:
    if block.type == "thinking":
        print(f"Thinking: {block.thinking}")
    elif block.type == "text":
        print(f"Response: {block.text}")
```

### Streaming Responses

For real-time responses:

```python
service = AnthropicService()

for chunk in service.stream_completion("Write a story..."):
    print(chunk, end='', flush=True)
```

## Available Models

- `claude-sonnet-4-5-20250929` - Latest Sonnet 4.5 (default)
- `claude-opus-4-5-20251101` - Latest Opus 4.5 (most capable)
- `claude-haiku-4-5-20250930` - Fastest, most cost-effective

Choose based on your needs:
- **Quality**: Opus > Sonnet > Haiku
- **Speed**: Haiku > Sonnet > Opus
- **Cost**: Haiku < Sonnet < Opus

## Troubleshooting

### API Key Not Found

**Error**: `ValueError: Anthropic API key not found`

**Solution**: Ensure `ANTHROPIC_API_KEY` is set in your `.env` file or environment variables.

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'anthropic'`

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

### Rate Limiting

**Error**: `429 Too Many Requests`

**Solution**: The LLM orchestrator includes automatic retry logic with exponential backoff. For direct SDK usage, implement rate limiting or upgrade your API plan.

### Timeout Errors

**Error**: Request times out

**Solution**: Increase timeout or reduce `max_tokens`:
```python
service.simple_completion(prompt, max_tokens=2048)  # Lower token limit
```

## Best Practices

1. **Use Environment Variables**: Never hardcode API keys in your code
2. **Enable Thinking for Complex Tasks**: Use extended thinking for reasoning-heavy tasks
3. **Choose the Right Model**: Balance cost, speed, and quality based on your use case
4. **Implement Error Handling**: Always wrap API calls in try-except blocks
5. **Monitor Usage**: Track token usage to optimize costs

## Additional Resources

- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Claude Model Comparison](https://docs.anthropic.com/en/docs/models-overview)
- [Extended Thinking Guide](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking)
- [Anthropic Console](https://console.anthropic.com/) - Manage API keys and usage
