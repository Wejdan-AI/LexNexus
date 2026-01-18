"""
WejdanAI Utilities
===================
Helper functions for the RAG system.
"""

import hashlib
import os
import re
from typing import Any, Optional


def mask_pii(text: str) -> str:
    """
    Mask personally identifiable information in text.

    Args:
        text: Input text potentially containing PII

    Returns:
        Text with PII masked
    """
    # Email addresses
    text = re.sub(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        '[EMAIL]',
        text,
    )

    # Phone numbers (various formats)
    text = re.sub(
        r'\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b',
        '[PHONE]',
        text,
    )

    # Saudi phone numbers
    text = re.sub(
        r'\b(?:\+966|00966|05)[0-9]{8,9}\b',
        '[PHONE_SA]',
        text,
    )

    # Social Security Numbers (US)
    text = re.sub(
        r'\b[0-9]{3}-[0-9]{2}-[0-9]{4}\b',
        '[SSN]',
        text,
    )

    # Saudi National ID
    text = re.sub(
        r'\b[12][0-9]{9}\b',
        '[NATIONAL_ID]',
        text,
    )

    # Credit card numbers
    text = re.sub(
        r'\b(?:[0-9]{4}[-\s]?){3}[0-9]{4}\b',
        '[CREDIT_CARD]',
        text,
    )

    # IP addresses
    text = re.sub(
        r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
        '[IP_ADDRESS]',
        text,
    )

    return text


def generate_id(content: str, prefix: str = "") -> str:
    """
    Generate a stable ID from content.

    Args:
        content: Content to hash
        prefix: Optional prefix for the ID

    Returns:
        A unique, stable ID
    """
    hash_value = hashlib.sha256(content.encode()).hexdigest()[:16]
    return f"{prefix}{hash_value}" if prefix else hash_value


def truncate_text(text: str, max_length: int = 1000, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add when truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 100,
) -> list[str]:
    """
    Split text into overlapping chunks.

    Args:
        text: Text to split
        chunk_size: Size of each chunk
        overlap: Overlap between chunks

    Returns:
        List of text chunks
    """
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # Try to break at a sentence boundary
        if end < len(text):
            # Look for sentence endings
            for sep in ['. ', '.\n', '! ', '? ', '\n\n']:
                idx = text.rfind(sep, start, end)
                if idx > start:
                    end = idx + len(sep)
                    break

        chunks.append(text[start:end].strip())
        start = end - overlap

    return chunks


def detect_language(text: str) -> str:
    """
    Simple language detection.

    Args:
        text: Text to analyze

    Returns:
        Language code ("ar", "zh", "en")
    """
    # Arabic character range
    arabic_chars = len(re.findall(r'[\u0600-\u06FF]', text))

    # Chinese character range
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))

    # Total characters (excluding spaces/punctuation)
    total = len(re.findall(r'\w', text))

    if total == 0:
        return "en"

    arabic_ratio = arabic_chars / total
    chinese_ratio = chinese_chars / total

    if arabic_ratio > 0.3:
        return "ar"
    elif chinese_ratio > 0.3:
        return "zh"

    return "en"


def format_tokens(count: int) -> str:
    """
    Format token count for display.

    Args:
        count: Token count

    Returns:
        Formatted string
    """
    if count >= 1_000_000:
        return f"{count / 1_000_000:.1f}M"
    elif count >= 1_000:
        return f"{count / 1_000:.1f}K"
    return str(count)


def format_cost(amount: float) -> str:
    """
    Format cost amount for display.

    Args:
        amount: Cost in dollars

    Returns:
        Formatted string
    """
    if amount < 0.01:
        return f"${amount:.4f}"
    elif amount < 1:
        return f"${amount:.3f}"
    return f"${amount:.2f}"


def get_env_or_raise(key: str, default: Optional[str] = None) -> str:
    """
    Get environment variable or raise error.

    Args:
        key: Environment variable name
        default: Default value if not set

    Returns:
        The value

    Raises:
        ValueError: If not set and no default
    """
    value = os.getenv(key, default)
    if value is None:
        raise ValueError(f"Environment variable {key} is required")
    return value


def safe_json_loads(text: str, default: Any = None) -> Any:
    """
    Safely parse JSON with a default value.

    Args:
        text: JSON string
        default: Default if parsing fails

    Returns:
        Parsed value or default
    """
    import json
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return default
