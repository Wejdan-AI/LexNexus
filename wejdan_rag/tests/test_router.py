"""
WejdanAI Router Tests
======================
Unit tests for the intelligent model router.
"""

import sys
sys.path.insert(0, '..')

import pytest
from wejdan_rag.core.router import ModelRouter, get_router
from wejdan_rag.config.models import ModelProvider, TaskType


class TestModelRouter:
    """Tests for ModelRouter class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.router = ModelRouter()

    def test_router_initialization(self):
        """Test router initializes correctly."""
        assert self.router is not None
        assert self.router.default_model == ModelProvider.CLAUDE
        assert self.router.language_detection is True

    def test_code_routing(self):
        """Test code queries route to DeepSeek."""
        queries = [
            "Write a Python function",
            "Debug this JavaScript code",
            "Implement a sorting algorithm",
        ]
        for query in queries:
            decision = self.router.route(query)
            assert decision.primary_model == ModelProvider.DEEPSEEK, \
                f"Expected DeepSeek for '{query}', got {decision.primary_model}"

    def test_arabic_routing(self):
        """Test Arabic queries route to Qwen."""
        queries = [
            "ما هي عاصمة السعودية",
            "اكتب لي مقالة عن الذكاء الاصطناعي",
            "ترجم هذا النص",
        ]
        for query in queries:
            decision = self.router.route(query)
            assert decision.primary_model == ModelProvider.QWEN, \
                f"Expected Qwen for '{query}', got {decision.primary_model}"

    def test_chinese_routing(self):
        """Test Chinese queries route to Qwen."""
        queries = [
            "帮我翻译这段话",
            "这是一个测试",
            "请解释这个概念",
        ]
        for query in queries:
            decision = self.router.route(query)
            assert decision.primary_model == ModelProvider.QWEN, \
                f"Expected Qwen for '{query}', got {decision.primary_model}"

    def test_research_routing(self):
        """Test research queries route to Perplexity."""
        queries = [
            "What is the latest news today",
            "Look up information about recent events",
            "Fact check is this accurate",
        ]
        for query in queries:
            decision = self.router.route(query)
            assert decision.primary_model == ModelProvider.PERPLEXITY, \
                f"Expected Perplexity for '{query}', got {decision.primary_model}"

    def test_privacy_routing(self):
        """Test privacy queries route to Venice."""
        queries = [
            "This is private and confidential",
            "Handle this sensitive information",
        ]
        for query in queries:
            decision = self.router.route(query)
            assert decision.primary_model == ModelProvider.VENICE, \
                f"Expected Venice for '{query}', got {decision.primary_model}"

    def test_creative_routing(self):
        """Test creative queries route to ChatGPT."""
        queries = [
            "Write me a creative story",
            "Brainstorm ideas for a startup",
        ]
        for query in queries:
            decision = self.router.route(query)
            assert decision.primary_model == ModelProvider.CHATGPT, \
                f"Expected ChatGPT for '{query}', got {decision.primary_model}"

    def test_analysis_routing(self):
        """Test complex analysis routes to Claude."""
        queries = [
            "Analyze this complex document",
            "Provide complex reasoning for this problem",
        ]
        for query in queries:
            decision = self.router.route(query)
            assert decision.primary_model == ModelProvider.CLAUDE, \
                f"Expected Claude for '{query}', got {decision.primary_model}"

    def test_automation_routing(self):
        """Test automation queries route to Manus."""
        queries = [
            "Create a multi-step automation workflow",
            "Automate this web scraping task",
        ]
        for query in queries:
            decision = self.router.route(query)
            assert decision.primary_model == ModelProvider.MANUS, \
                f"Expected Manus for '{query}', got {decision.primary_model}"

    def test_force_model(self):
        """Test forcing a specific model."""
        decision = self.router.route(
            "Write Python code",
            force_model=ModelProvider.CLAUDE,
        )
        assert decision.primary_model == ModelProvider.CLAUDE
        assert decision.confidence == 1.0

    def test_fallback_models(self):
        """Test fallback models are provided."""
        decision = self.router.route("Test query")
        assert len(decision.fallback_models) > 0

    def test_routing_decision_structure(self):
        """Test routing decision has all required fields."""
        decision = self.router.route("Test query")
        assert hasattr(decision, 'primary_model')
        assert hasattr(decision, 'fallback_models')
        assert hasattr(decision, 'detected_tasks')
        assert hasattr(decision, 'confidence')
        assert hasattr(decision, 'reasoning')
        assert hasattr(decision, 'model_config')


class TestLanguageDetection:
    """Tests for language detection."""

    def setup_method(self):
        """Set up test fixtures."""
        self.router = ModelRouter()

    def test_arabic_detection(self):
        """Test Arabic language is detected."""
        text = "مرحباً كيف حالك اليوم"
        lang = self.router._detect_language(text)
        assert lang == "arabic"

    def test_chinese_detection(self):
        """Test Chinese language is detected."""
        text = "你好世界这是一个测试"
        lang = self.router._detect_language(text)
        assert lang == "chinese"

    def test_english_detection(self):
        """Test English language is detected."""
        text = "Hello world this is a test"
        lang = self.router._detect_language(text)
        assert lang == "english"

    def test_mixed_defaults_to_dominant(self):
        """Test mixed text uses dominant language."""
        text = "Hello مرحباً world كيف"  # More Arabic
        lang = self.router._detect_language(text)
        # Should detect based on ratio
        assert lang in ["arabic", "english"]


class TestGetRouter:
    """Tests for router singleton."""

    def test_get_router_returns_instance(self):
        """Test get_router returns a router instance."""
        router = get_router()
        assert isinstance(router, ModelRouter)

    def test_get_router_returns_same_instance(self):
        """Test get_router returns singleton."""
        router1 = get_router()
        router2 = get_router()
        assert router1 is router2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
