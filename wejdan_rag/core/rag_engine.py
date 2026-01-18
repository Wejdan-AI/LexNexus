"""
WejdanAI RAG Engine
====================
Retrieval-Augmented Generation engine with Notion integration.
"""

import hashlib
import json
import os
import re
from dataclasses import dataclass, field
from typing import Any, Optional

import httpx

from ..config.models import ModelProvider
from ..providers import ClaudeProvider, CompletionResponse, Message
from .router import ModelRouter, RoutingDecision, get_router


@dataclass
class Document:
    """A retrieved document for RAG context."""
    id: str
    content: str
    title: str = ""
    source: str = ""
    score: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RAGResponse:
    """Response from RAG system."""
    answer: str
    model_used: ModelProvider
    documents: list[Document]
    routing_decision: RoutingDecision
    completion: CompletionResponse
    context_tokens: int = 0


class NotionRetriever:
    """Retrieves relevant documents from Notion databases."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        database_ids: Optional[list[str]] = None,
    ):
        self.api_key = api_key or os.getenv("NOTION_API_KEY")
        self.database_ids = database_ids or []
        self.base_url = "https://api.notion.com/v1"
        self._client: Optional[httpx.AsyncClient] = None

    @property
    def client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Notion-Version": "2022-06-28",
                    "Content-Type": "application/json",
                },
                timeout=30.0,
            )
        return self._client

    async def close(self):
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None

    def _extract_text_from_block(self, block: dict) -> str:
        """Extract text content from a Notion block."""
        block_type = block.get("type", "")
        block_content = block.get(block_type, {})

        if "rich_text" in block_content:
            return " ".join(
                rt.get("plain_text", "")
                for rt in block_content.get("rich_text", [])
            )
        elif "title" in block_content:
            return " ".join(
                rt.get("plain_text", "")
                for rt in block_content.get("title", [])
            )

        return ""

    def _extract_page_content(self, page: dict) -> tuple[str, str]:
        """Extract title and content from a Notion page."""
        properties = page.get("properties", {})
        title = ""
        content_parts = []

        # Extract title
        for prop_name, prop_value in properties.items():
            prop_type = prop_value.get("type", "")

            if prop_type == "title":
                title = " ".join(
                    rt.get("plain_text", "")
                    for rt in prop_value.get("title", [])
                )
            elif prop_type == "rich_text":
                text = " ".join(
                    rt.get("plain_text", "")
                    for rt in prop_value.get("rich_text", [])
                )
                if text:
                    content_parts.append(f"{prop_name}: {text}")

        content = "\n".join(content_parts)
        return title, content

    async def search(
        self,
        query: str,
        max_results: int = 5,
    ) -> list[Document]:
        """Search Notion for relevant documents."""
        if not self.api_key:
            return []

        documents = []

        try:
            # Use Notion search API
            response = await self.client.post(
                f"{self.base_url}/search",
                json={
                    "query": query,
                    "page_size": max_results,
                    "filter": {"property": "object", "value": "page"},
                },
            )
            response.raise_for_status()

            data = response.json()

            for result in data.get("results", []):
                title, content = self._extract_page_content(result)

                # Simple relevance score based on query match
                query_lower = query.lower()
                title_lower = title.lower()
                content_lower = content.lower()

                score = 0.0
                if query_lower in title_lower:
                    score += 0.6
                if query_lower in content_lower:
                    score += 0.4

                # Partial word matching
                query_words = query_lower.split()
                for word in query_words:
                    if word in title_lower:
                        score += 0.1
                    if word in content_lower:
                        score += 0.05

                doc = Document(
                    id=result.get("id", ""),
                    title=title,
                    content=content or title,
                    source=result.get("url", ""),
                    score=min(score, 1.0),
                    metadata={
                        "created_time": result.get("created_time"),
                        "last_edited_time": result.get("last_edited_time"),
                    },
                )
                documents.append(doc)

        except Exception as e:
            print(f"Notion search error: {e}")

        # Sort by score
        documents.sort(key=lambda d: d.score, reverse=True)
        return documents[:max_results]

    async def get_database_content(
        self,
        database_id: str,
        max_pages: int = 100,
    ) -> list[Document]:
        """Get all pages from a Notion database."""
        documents = []

        try:
            response = await self.client.post(
                f"{self.base_url}/databases/{database_id}/query",
                json={"page_size": min(max_pages, 100)},
            )
            response.raise_for_status()

            data = response.json()

            for page in data.get("results", []):
                title, content = self._extract_page_content(page)

                doc = Document(
                    id=page.get("id", ""),
                    title=title,
                    content=content or title,
                    source=page.get("url", ""),
                    score=1.0,
                    metadata={
                        "database_id": database_id,
                        "created_time": page.get("created_time"),
                    },
                )
                documents.append(doc)

        except Exception as e:
            print(f"Database query error: {e}")

        return documents


class VectorStore:
    """Simple in-memory vector store for document retrieval."""

    def __init__(self):
        self.documents: dict[str, Document] = {}
        self._embeddings: dict[str, list[float]] = {}

    def _simple_embedding(self, text: str) -> list[float]:
        """
        Simple text-based embedding using character/word frequencies.
        For production, use OpenAI/Cohere embeddings.
        """
        # Normalize text
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)

        # Character frequencies (256 dimensions)
        char_freq = [0.0] * 256
        for char in text:
            idx = ord(char) % 256
            char_freq[idx] += 1

        # Normalize
        total = sum(char_freq) or 1
        char_freq = [f / total for f in char_freq]

        return char_freq

    def _cosine_similarity(
        self,
        vec1: list[float],
        vec2: list[float],
    ) -> float:
        """Calculate cosine similarity between two vectors."""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a * a for a in vec1) ** 0.5
        norm2 = sum(b * b for b in vec2) ** 0.5

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def add(self, document: Document):
        """Add a document to the store."""
        self.documents[document.id] = document
        self._embeddings[document.id] = self._simple_embedding(
            f"{document.title} {document.content}"
        )

    def add_many(self, documents: list[Document]):
        """Add multiple documents."""
        for doc in documents:
            self.add(doc)

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[Document]:
        """Search for similar documents."""
        if not self.documents:
            return []

        query_embedding = self._simple_embedding(query)

        # Calculate similarities
        scored_docs = []
        for doc_id, doc_embedding in self._embeddings.items():
            similarity = self._cosine_similarity(query_embedding, doc_embedding)
            doc = self.documents[doc_id]
            doc.score = similarity
            scored_docs.append(doc)

        # Sort by similarity
        scored_docs.sort(key=lambda d: d.score, reverse=True)

        return scored_docs[:top_k]

    def clear(self):
        """Clear all documents."""
        self.documents.clear()
        self._embeddings.clear()


class RAGEngine:
    """
    Main RAG engine that combines retrieval with multi-model generation.
    """

    def __init__(
        self,
        api_keys: Optional[dict[str, str]] = None,
        notion_database_ids: Optional[list[str]] = None,
        router: Optional[ModelRouter] = None,
    ):
        self.api_keys = api_keys or {}
        self.router = router or get_router()

        # Initialize retrievers
        self.notion = NotionRetriever(
            api_key=self.api_keys.get("notion") or os.getenv("NOTION_API_KEY"),
            database_ids=notion_database_ids or [],
        )

        # Initialize vector store for caching
        self.vector_store = VectorStore()

        # Provider instances (lazy loaded)
        self._providers: dict[ModelProvider, Any] = {}

    def _get_provider(self, provider: ModelProvider):
        """Get or create a provider instance."""
        if provider not in self._providers:
            api_key = self._get_api_key(provider)

            from ..providers import (
                ClaudeProvider,
                CopilotProvider,
                DeepSeekProvider,
                GeminiProvider,
                ManusProvider,
                OpenAIProvider,
                PerplexityProvider,
                QwenProvider,
                VeniceProvider,
            )

            provider_map = {
                ModelProvider.CHATGPT: OpenAIProvider,
                ModelProvider.GEMINI: GeminiProvider,
                ModelProvider.DEEPSEEK: DeepSeekProvider,
                ModelProvider.PERPLEXITY: PerplexityProvider,
                ModelProvider.QWEN: QwenProvider,
                ModelProvider.VENICE: VeniceProvider,
                ModelProvider.CLAUDE: ClaudeProvider,
                ModelProvider.COPILOT: CopilotProvider,
                ModelProvider.MANUS: ManusProvider,
            }

            provider_class = provider_map.get(provider)
            if provider_class:
                self._providers[provider] = provider_class(api_key=api_key)

        return self._providers.get(provider)

    def _get_api_key(self, provider: ModelProvider) -> Optional[str]:
        """Get API key for a provider."""
        key_map = {
            ModelProvider.CHATGPT: "OPENAI_API_KEY",
            ModelProvider.GEMINI: "GOOGLE_API_KEY",
            ModelProvider.DEEPSEEK: "DEEPSEEK_API_KEY",
            ModelProvider.PERPLEXITY: "PERPLEXITY_API_KEY",
            ModelProvider.QWEN: "QWEN_API_KEY",
            ModelProvider.VENICE: "VENICE_API_KEY",
            ModelProvider.CLAUDE: "ANTHROPIC_API_KEY",
            ModelProvider.COPILOT: "AZURE_API_KEY",
            ModelProvider.MANUS: "MANUS_API_KEY",
        }

        env_var = key_map.get(provider, "")
        return self.api_keys.get(provider.value) or os.getenv(env_var)

    def _build_context(self, documents: list[Document]) -> str:
        """Build context string from retrieved documents."""
        if not documents:
            return ""

        context_parts = ["## Retrieved Context\n"]

        for i, doc in enumerate(documents, 1):
            context_parts.append(
                f"### [{i}] {doc.title}\n"
                f"{doc.content}\n"
                f"(Source: {doc.source})\n"
            )

        return "\n".join(context_parts)

    async def retrieve(
        self,
        query: str,
        sources: Optional[list[str]] = None,
        max_docs: int = 5,
    ) -> list[Document]:
        """
        Retrieve relevant documents from all sources.

        Args:
            query: The search query
            sources: List of sources to search ("notion", "vector")
            max_docs: Maximum documents to return
        """
        sources = sources or ["notion", "vector"]
        all_docs = []

        # Search Notion
        if "notion" in sources:
            notion_docs = await self.notion.search(query, max_docs)
            all_docs.extend(notion_docs)

            # Cache in vector store
            self.vector_store.add_many(notion_docs)

        # Search vector store
        if "vector" in sources:
            vector_docs = self.vector_store.search(query, max_docs)
            # Avoid duplicates
            existing_ids = {d.id for d in all_docs}
            for doc in vector_docs:
                if doc.id not in existing_ids:
                    all_docs.append(doc)

        # Sort by score and limit
        all_docs.sort(key=lambda d: d.score, reverse=True)
        return all_docs[:max_docs]

    async def query(
        self,
        question: str,
        attachments: Optional[list] = None,
        use_rag: bool = True,
        max_docs: int = 5,
        preferences: Optional[dict] = None,
        force_model: Optional[ModelProvider] = None,
        system_prompt: Optional[str] = None,
    ) -> RAGResponse:
        """
        Process a query using RAG with intelligent model routing.

        Args:
            question: The user's question
            attachments: Optional images/files
            use_rag: Whether to retrieve context
            max_docs: Maximum documents for context
            preferences: Routing preferences (prefer_cost, prefer_quality, prefer_privacy)
            force_model: Force a specific model
            system_prompt: Override system prompt
        """
        # Route to appropriate model
        routing = self.router.route(
            query=question,
            attachments=attachments,
            preferences=preferences,
            force_model=force_model,
        )

        # Retrieve context if enabled
        documents = []
        context = ""

        if use_rag:
            documents = await self.retrieve(question, max_docs=max_docs)
            context = self._build_context(documents)

        # Build system prompt
        if not system_prompt:
            system_prompt = (
                "You are WejdanAI, an intelligent assistant with access to "
                "a knowledge base. Answer questions accurately using the "
                "provided context when relevant. If the context doesn't help, "
                "use your own knowledge.\n\n"
                f"{context}"
            )
        elif context:
            system_prompt = f"{system_prompt}\n\n{context}"

        # Get provider
        provider = self._get_provider(routing.primary_model)

        if not provider:
            # Fallback to Claude if provider not available
            provider = self._get_provider(ModelProvider.CLAUDE)
            routing.primary_model = ModelProvider.CLAUDE

        # Generate response
        messages = [Message(role="user", content=question)]

        completion = await provider.complete(
            messages=messages,
            system_prompt=system_prompt,
        )

        # Try fallbacks if failed
        if not completion.success and routing.fallback_models:
            for fallback in routing.fallback_models:
                fallback_provider = self._get_provider(fallback)
                if fallback_provider:
                    completion = await fallback_provider.complete(
                        messages=messages,
                        system_prompt=system_prompt,
                    )
                    if completion.success:
                        routing.primary_model = fallback
                        break

        return RAGResponse(
            answer=completion.content,
            model_used=routing.primary_model,
            documents=documents,
            routing_decision=routing,
            completion=completion,
            context_tokens=len(context.split()),
        )

    async def close(self):
        """Close all connections."""
        await self.notion.close()
        for provider in self._providers.values():
            if hasattr(provider, 'close'):
                await provider.close()


# Singleton instance
_engine: Optional[RAGEngine] = None


def get_engine(**kwargs) -> RAGEngine:
    """Get the global RAG engine instance."""
    global _engine
    if _engine is None:
        _engine = RAGEngine(**kwargs)
    return _engine
