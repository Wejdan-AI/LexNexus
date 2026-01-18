"""
WejdanAI - Multi-Model RAG System
==================================

A powerful RAG (Retrieval-Augmented Generation) system that intelligently
routes requests to the most appropriate AI model based on task analysis.

Supported Models:
- ChatGPT: Creative writing, brainstorming, general tasks
- Gemini: Google integration, multimodal, image analysis
- DeepSeek: Code generation, technical tasks, algorithms
- Perplexity: Research with citations, fact-checking, current events
- Qwen: Arabic/Chinese content, multilingual tasks
- Venice AI: Privacy-sensitive tasks, uncensored content
- Copilot: Microsoft Office, enterprise workflows
- Manus: Autonomous multi-step tasks, web automation
- Claude: Analysis, long documents, orchestration, complex reasoning

Usage:
    from wejdan_rag import RAGEngine, get_engine

    # Get the singleton engine
    engine = get_engine()

    # Query with automatic model routing
    result = await engine.query("Write me a Python function")

    # Force a specific model
    result = await engine.query(
        "Analyze this document",
        force_model=ModelProvider.CLAUDE,
    )

    # Optimize for cost
    result = await engine.query(
        "Translate this to Arabic",
        preferences={"prefer_cost": True},
    )

API Server:
    uvicorn wejdan_rag.api:app --reload

Environment Variables:
    OPENAI_API_KEY - For ChatGPT
    GOOGLE_API_KEY - For Gemini
    DEEPSEEK_API_KEY - For DeepSeek
    PERPLEXITY_API_KEY - For Perplexity
    QWEN_API_KEY - For Qwen
    VENICE_API_KEY - For Venice AI
    ANTHROPIC_API_KEY - For Claude
    AZURE_API_KEY - For Copilot
    MANUS_API_KEY - For Manus
    NOTION_API_KEY - For Notion integration
"""

__version__ = "1.0.0"
__author__ = "WejdanAI Team"

# Core exports
from .config import (
    MODELS,
    ModelConfig,
    ModelProvider,
    TaskType,
)

from .core import (
    Document,
    ModelRouter,
    RAGEngine,
    RAGResponse,
    RoutingDecision,
    get_engine,
    get_router,
)

from .providers import (
    BaseProvider,
    ClaudeProvider,
    CompletionResponse,
    DeepSeekProvider,
    GeminiProvider,
    ManusProvider,
    Message,
    OpenAIProvider,
    PerplexityProvider,
    QwenProvider,
    VeniceProvider,
)

from .utils import (
    chunk_text,
    detect_language,
    mask_pii,
    truncate_text,
)

__all__ = [
    # Version
    "__version__",
    # Config
    "MODELS",
    "ModelConfig",
    "ModelProvider",
    "TaskType",
    # Core
    "RAGEngine",
    "RAGResponse",
    "Document",
    "ModelRouter",
    "RoutingDecision",
    "get_engine",
    "get_router",
    # Providers
    "BaseProvider",
    "Message",
    "CompletionResponse",
    "OpenAIProvider",
    "GeminiProvider",
    "DeepSeekProvider",
    "PerplexityProvider",
    "QwenProvider",
    "VeniceProvider",
    "ClaudeProvider",
    "ManusProvider",
    # Utils
    "mask_pii",
    "chunk_text",
    "truncate_text",
    "detect_language",
]
