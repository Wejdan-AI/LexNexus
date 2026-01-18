#!/usr/bin/env python3
"""
WejdanAI Usage Examples
========================

Examples of using the multi-model RAG system.
"""

import asyncio
import os

# Set API keys (or use environment variables)
# os.environ["OPENAI_API_KEY"] = "your-key"
# os.environ["ANTHROPIC_API_KEY"] = "your-key"
# os.environ["NOTION_API_KEY"] = "your-key"


async def basic_query():
    """Basic query with automatic model routing."""
    from wejdan_rag import get_engine

    engine = get_engine()

    # The system automatically routes to the best model
    result = await engine.query(
        "What are the best practices for Python error handling?"
    )

    print(f"Answer: {result.answer}")
    print(f"Model: {result.model_used.value}")
    print(f"Confidence: {result.routing_decision.confidence:.0%}")


async def code_generation():
    """Code generation - routes to DeepSeek."""
    from wejdan_rag import get_engine

    engine = get_engine()

    result = await engine.query(
        "Write a Python function to find the longest palindromic substring"
    )

    print(f"Model used: {result.model_used.value}")
    print(f"Code:\n{result.answer}")


async def arabic_content():
    """Arabic content - routes to Qwen."""
    from wejdan_rag import get_engine

    engine = get_engine()

    result = await engine.query(
        "اكتب لي مقالة قصيرة عن الذكاء الاصطناعي"
    )

    print(f"Model used: {result.model_used.value}")
    print(f"Answer: {result.answer}")


async def research_with_citations():
    """Research - routes to Perplexity."""
    from wejdan_rag import get_engine

    engine = get_engine()

    result = await engine.query(
        "What are the latest developments in quantum computing in 2024?"
    )

    print(f"Model used: {result.model_used.value}")
    print(f"Answer: {result.answer}")
    print(f"Citations: {result.completion.citations}")


async def privacy_mode():
    """Privacy-sensitive query - routes to Venice."""
    from wejdan_rag import get_engine

    engine = get_engine()

    result = await engine.query(
        "This is private and confidential information",
        preferences={"prefer_privacy": True},
    )

    print(f"Model used: {result.model_used.value}")
    print(f"Privacy mode: {result.completion.metadata.get('privacy_mode', False)}")


async def force_model():
    """Force a specific model."""
    from wejdan_rag import get_engine, ModelProvider

    engine = get_engine()

    result = await engine.query(
        "Analyze this complex problem",
        force_model=ModelProvider.CLAUDE,
    )

    print(f"Model used: {result.model_used.value}")
    print(f"Answer: {result.answer}")


async def with_rag_context():
    """Query with RAG context from Notion."""
    from wejdan_rag import get_engine

    engine = get_engine()

    # This will search Notion for relevant documents
    result = await engine.query(
        "What are the banking compliance requirements?",
        use_rag=True,
        max_docs=5,
    )

    print(f"Model used: {result.model_used.value}")
    print(f"Documents used: {len(result.documents)}")
    print(f"Answer: {result.answer}")


async def analyze_routing():
    """Analyze how a query would be routed."""
    from wejdan_rag import get_router

    router = get_router()

    queries = [
        "Write a Python function",
        "What's the latest news about AI?",
        "ترجم هذا النص إلى الإنجليزية",
        "Analyze this image",
        "Create a multi-step automation workflow",
    ]

    for query in queries:
        decision = router.route(query)
        print(f"\nQuery: {query}")
        print(f"  → Model: {decision.model_config.name}")
        print(f"  → Confidence: {decision.confidence:.0%}")
        print(f"  → Tasks: {[t.value for t in decision.detected_tasks]}")


async def main():
    """Run all examples."""
    print("=" * 60)
    print("WejdanAI Multi-Model RAG System Examples")
    print("=" * 60)

    print("\n1. Analyzing Routing")
    print("-" * 40)
    await analyze_routing()

    # Uncomment to run queries (requires API keys)
    # print("\n2. Basic Query")
    # await basic_query()

    # print("\n3. Code Generation")
    # await code_generation()

    # print("\n4. Arabic Content")
    # await arabic_content()

    print("\n" + "=" * 60)
    print("Examples complete!")


if __name__ == "__main__":
    asyncio.run(main())
