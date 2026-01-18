"""
WejdanAI Configuration
=======================
Configuration for the multi-model RAG system.
"""

from .models import (
    MODELS,
    TASK_KEYWORDS,
    TASK_MODEL_MAP,
    ModelConfig,
    ModelProvider,
    TaskType,
)

__all__ = [
    "MODELS",
    "ModelConfig",
    "ModelProvider",
    "TaskType",
    "TASK_MODEL_MAP",
    "TASK_KEYWORDS",
]
