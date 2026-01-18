"""
WejdanAI Intelligent Model Router
==================================
Routes requests to the most appropriate AI model based on task analysis.
"""

import re
from dataclasses import dataclass
from typing import Optional

from ..config.models import (
    MODELS,
    TASK_KEYWORDS,
    TASK_MODEL_MAP,
    ModelConfig,
    ModelProvider,
    TaskType,
)


@dataclass
class RoutingDecision:
    """Result of the routing decision."""
    primary_model: ModelProvider
    fallback_models: list[ModelProvider]
    detected_tasks: list[TaskType]
    confidence: float
    reasoning: str
    model_config: ModelConfig


class ModelRouter:
    """
    Intelligent router that analyzes requests and routes them
    to the most appropriate AI model.
    """

    def __init__(
        self,
        default_model: ModelProvider = ModelProvider.CLAUDE,
        language_detection: bool = True,
    ):
        self.default_model = default_model
        self.language_detection = language_detection
        self._task_patterns = self._compile_patterns()

    def _compile_patterns(self) -> dict[TaskType, re.Pattern]:
        """Compile regex patterns for task detection."""
        patterns = {}
        for task, keywords in TASK_KEYWORDS.items():
            # Create pattern that matches any keyword
            pattern_str = "|".join(
                re.escape(kw) for kw in keywords
            )
            patterns[task] = re.compile(
                pattern_str, re.IGNORECASE | re.UNICODE
            )
        return patterns

    def _detect_language(self, text: str) -> Optional[str]:
        """Detect the primary language of the text."""
        # Arabic detection - count actual characters
        arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F]')
        arabic_chars = len(arabic_pattern.findall(text))

        # Chinese detection - count actual characters
        chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
        chinese_chars = len(chinese_pattern.findall(text))

        # Count only alphanumeric and script characters
        total_chars = len(re.findall(r'[\w\u0600-\u06FF\u4e00-\u9fff]', text))
        if total_chars == 0:
            return None

        arabic_ratio = arabic_chars / total_chars
        chinese_ratio = chinese_chars / total_chars

        if arabic_ratio > 0.3:
            return "arabic"
        elif chinese_ratio > 0.3:
            return "chinese"
        return "english"

    def _detect_tasks(self, query: str) -> list[tuple[TaskType, float]]:
        """
        Detect task types from the query.
        Returns list of (TaskType, confidence) tuples.
        """
        detected = []

        for task, pattern in self._task_patterns.items():
            matches = pattern.findall(query)
            if matches:
                # More matches = higher confidence
                confidence = min(len(matches) * 0.3, 1.0)
                detected.append((task, confidence))

        # Sort by confidence
        detected.sort(key=lambda x: x[1], reverse=True)
        return detected

    def _has_image_content(self, attachments: Optional[list] = None) -> bool:
        """Check if the request contains image content."""
        if not attachments:
            return False
        image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp'}
        for attachment in attachments:
            if isinstance(attachment, str):
                if any(attachment.lower().endswith(ext) for ext in image_extensions):
                    return True
            elif isinstance(attachment, dict) and attachment.get('type') == 'image':
                return True
        return False

    def _select_model(
        self,
        tasks: list[tuple[TaskType, float]],
        language: Optional[str],
        has_images: bool,
        preferences: Optional[dict] = None,
    ) -> tuple[ModelProvider, list[ModelProvider], float, str]:
        """
        Select the best model based on detected tasks and context.
        Returns (primary_model, fallbacks, confidence, reasoning).
        """
        reasoning_parts = []

        # Check for image content first
        if has_images:
            reasoning_parts.append("Image content detected")
            # Prioritize vision-capable models
            if TaskType.IMAGE_ANALYSIS in [t[0] for t in tasks]:
                return (
                    ModelProvider.GEMINI,
                    [ModelProvider.CHATGPT, ModelProvider.CLAUDE],
                    0.9,
                    "Image analysis task with image content -> Gemini",
                )

        # Check for language-specific routing
        if language == "arabic":
            reasoning_parts.append("Arabic language detected")
            tasks.insert(0, (TaskType.ARABIC_CONTENT, 0.8))
        elif language == "chinese":
            reasoning_parts.append("Chinese language detected")
            tasks.insert(0, (TaskType.CHINESE_CONTENT, 0.8))

        # No specific tasks detected
        if not tasks:
            return (
                self.default_model,
                [ModelProvider.CHATGPT, ModelProvider.GEMINI],
                0.5,
                "No specific task detected, using default model",
            )

        # Get the highest priority task
        primary_task, task_confidence = tasks[0]
        reasoning_parts.append(f"Primary task: {primary_task.value}")

        # Get models for this task
        suitable_models = TASK_MODEL_MAP.get(primary_task, [])

        if not suitable_models:
            return (
                self.default_model,
                [ModelProvider.CHATGPT],
                0.4,
                f"No specialized model for {primary_task.value}, using default",
            )

        # Filter by enabled models
        available_models = [
            m for m in suitable_models
            if MODELS[m].enabled
        ]

        if not available_models:
            return (
                self.default_model,
                [],
                0.3,
                "No available models for task, using default",
            )

        # Apply preferences if provided
        if preferences:
            if preferences.get("prefer_cost"):
                # Sort by cost
                available_models.sort(
                    key=lambda m: MODELS[m].cost_per_1k_tokens
                )
                reasoning_parts.append("Optimizing for cost")
            elif preferences.get("prefer_quality"):
                # Keep priority order (already sorted by quality)
                reasoning_parts.append("Optimizing for quality")
            elif preferences.get("prefer_privacy"):
                # Prioritize Venice for privacy
                if ModelProvider.VENICE in available_models:
                    available_models.remove(ModelProvider.VENICE)
                    available_models.insert(0, ModelProvider.VENICE)
                reasoning_parts.append("Optimizing for privacy")

        primary = available_models[0]
        fallbacks = available_models[1:3] if len(available_models) > 1 else []

        # Add general fallbacks if needed
        if len(fallbacks) < 2:
            for fallback in [ModelProvider.CLAUDE, ModelProvider.CHATGPT]:
                if fallback not in fallbacks and fallback != primary:
                    fallbacks.append(fallback)
                    if len(fallbacks) >= 2:
                        break

        confidence = task_confidence * 0.9  # Slight reduction for routing uncertainty

        reasoning = " -> ".join(reasoning_parts) + f" -> {primary.value}"

        return primary, fallbacks, confidence, reasoning

    def route(
        self,
        query: str,
        attachments: Optional[list] = None,
        preferences: Optional[dict] = None,
        force_model: Optional[ModelProvider] = None,
    ) -> RoutingDecision:
        """
        Route a query to the appropriate model.

        Args:
            query: The user's query text
            attachments: Optional list of attachments (images, files)
            preferences: Optional dict with 'prefer_cost', 'prefer_quality', 'prefer_privacy'
            force_model: Force routing to a specific model

        Returns:
            RoutingDecision with selected model and reasoning
        """
        # Handle forced model
        if force_model:
            config = MODELS[force_model]
            return RoutingDecision(
                primary_model=force_model,
                fallback_models=[],
                detected_tasks=[],
                confidence=1.0,
                reasoning=f"Model forced to {force_model.value}",
                model_config=config,
            )

        # Detect language
        language = self._detect_language(query) if self.language_detection else None

        # Detect tasks
        tasks = self._detect_tasks(query)
        detected_task_types = [t[0] for t in tasks]

        # Check for images
        has_images = self._has_image_content(attachments)

        # Select model
        primary, fallbacks, confidence, reasoning = self._select_model(
            tasks, language, has_images, preferences
        )

        return RoutingDecision(
            primary_model=primary,
            fallback_models=fallbacks,
            detected_tasks=detected_task_types,
            confidence=confidence,
            reasoning=reasoning,
            model_config=MODELS[primary],
        )

    def explain_routing(self, decision: RoutingDecision) -> str:
        """Generate a human-readable explanation of the routing decision."""
        lines = [
            f"🎯 Selected Model: {decision.model_config.name}",
            f"📊 Confidence: {decision.confidence:.0%}",
            f"💭 Reasoning: {decision.reasoning}",
        ]

        if decision.detected_tasks:
            tasks_str = ", ".join(t.value for t in decision.detected_tasks[:3])
            lines.append(f"📋 Detected Tasks: {tasks_str}")

        if decision.fallback_models:
            fallbacks_str = ", ".join(
                MODELS[m].name for m in decision.fallback_models
            )
            lines.append(f"🔄 Fallbacks: {fallbacks_str}")

        return "\n".join(lines)


# Singleton instance
_router: Optional[ModelRouter] = None


def get_router() -> ModelRouter:
    """Get the global router instance."""
    global _router
    if _router is None:
        _router = ModelRouter()
    return _router
