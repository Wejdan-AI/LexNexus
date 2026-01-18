"""
WejdanAI Multi-Model Configuration
===================================
Configuration for all AI models and their specializations.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class TaskType(Enum):
    """Types of tasks that can be routed to different models."""
    # Creative & General
    CREATIVE_WRITING = "creative_writing"
    BRAINSTORMING = "brainstorming"
    GENERAL = "general"

    # Technical
    CODE_GENERATION = "code_generation"
    CODE_REVIEW = "code_review"
    DEBUGGING = "debugging"
    ALGORITHMS = "algorithms"

    # Research & Analysis
    RESEARCH = "research"
    FACT_CHECKING = "fact_checking"
    CURRENT_EVENTS = "current_events"
    CITATIONS = "citations"

    # Multimodal
    IMAGE_ANALYSIS = "image_analysis"
    IMAGE_GENERATION = "image_generation"
    MULTIMODAL = "multimodal"

    # Language & Translation
    ARABIC_CONTENT = "arabic_content"
    CHINESE_CONTENT = "chinese_content"
    MULTILINGUAL = "multilingual"
    TRANSLATION = "translation"

    # Document & Analysis
    LONG_DOCUMENT = "long_document"
    COMPLEX_REASONING = "complex_reasoning"
    ANALYSIS = "analysis"
    ORCHESTRATION = "orchestration"

    # Enterprise & Automation
    OFFICE_INTEGRATION = "office_integration"
    ENTERPRISE = "enterprise"
    WEB_AUTOMATION = "web_automation"
    MULTI_STEP_TASK = "multi_step_task"

    # Privacy
    PRIVACY_SENSITIVE = "privacy_sensitive"
    UNCENSORED = "uncensored"


class ModelProvider(Enum):
    """Available AI model providers."""
    CHATGPT = "chatgpt"
    GEMINI = "gemini"
    DEEPSEEK = "deepseek"
    PERPLEXITY = "perplexity"
    QWEN = "qwen"
    VENICE = "venice"
    COPILOT = "copilot"
    MANUS = "manus"
    CLAUDE = "claude"


@dataclass
class ModelConfig:
    """Configuration for a single AI model."""
    provider: ModelProvider
    name: str
    description: str
    api_base: Optional[str] = None
    model_id: str = ""
    max_tokens: int = 4096
    temperature: float = 0.7
    supports_streaming: bool = True
    supports_vision: bool = False
    supports_function_calling: bool = False
    rate_limit_rpm: int = 60
    cost_per_1k_tokens: float = 0.0
    specializations: list[TaskType] = field(default_factory=list)
    priority: int = 1  # Lower = higher priority for tie-breaking
    enabled: bool = True


# Model Configurations
MODELS: dict[ModelProvider, ModelConfig] = {
    ModelProvider.CHATGPT: ModelConfig(
        provider=ModelProvider.CHATGPT,
        name="ChatGPT (GPT-4o)",
        description="Creative writing, brainstorming, general tasks",
        api_base="https://api.openai.com/v1",
        model_id="gpt-4o",
        max_tokens=16384,
        supports_vision=True,
        supports_function_calling=True,
        cost_per_1k_tokens=0.005,
        specializations=[
            TaskType.CREATIVE_WRITING,
            TaskType.BRAINSTORMING,
            TaskType.GENERAL,
        ],
        priority=2,
    ),

    ModelProvider.GEMINI: ModelConfig(
        provider=ModelProvider.GEMINI,
        name="Gemini Pro",
        description="Google integration, multimodal, image analysis",
        api_base="https://generativelanguage.googleapis.com/v1beta",
        model_id="gemini-1.5-pro",
        max_tokens=32768,
        supports_vision=True,
        supports_function_calling=True,
        cost_per_1k_tokens=0.00125,
        specializations=[
            TaskType.IMAGE_ANALYSIS,
            TaskType.MULTIMODAL,
            TaskType.IMAGE_GENERATION,
        ],
        priority=2,
    ),

    ModelProvider.DEEPSEEK: ModelConfig(
        provider=ModelProvider.DEEPSEEK,
        name="DeepSeek Coder",
        description="Code generation, technical tasks, algorithms",
        api_base="https://api.deepseek.com/v1",
        model_id="deepseek-coder",
        max_tokens=16384,
        supports_function_calling=True,
        cost_per_1k_tokens=0.0014,
        specializations=[
            TaskType.CODE_GENERATION,
            TaskType.CODE_REVIEW,
            TaskType.DEBUGGING,
            TaskType.ALGORITHMS,
        ],
        priority=1,
    ),

    ModelProvider.PERPLEXITY: ModelConfig(
        provider=ModelProvider.PERPLEXITY,
        name="Perplexity Sonar",
        description="Research with citations, fact-checking, current events",
        api_base="https://api.perplexity.ai",
        model_id="sonar-pro",
        max_tokens=8192,
        cost_per_1k_tokens=0.005,
        specializations=[
            TaskType.RESEARCH,
            TaskType.FACT_CHECKING,
            TaskType.CURRENT_EVENTS,
            TaskType.CITATIONS,
        ],
        priority=1,
    ),

    ModelProvider.QWEN: ModelConfig(
        provider=ModelProvider.QWEN,
        name="Qwen 2.5",
        description="Arabic/Chinese content, multilingual tasks",
        api_base="https://dashscope.aliyuncs.com/api/v1",
        model_id="qwen-max",
        max_tokens=32768,
        supports_vision=True,
        cost_per_1k_tokens=0.002,
        specializations=[
            TaskType.ARABIC_CONTENT,
            TaskType.CHINESE_CONTENT,
            TaskType.MULTILINGUAL,
            TaskType.TRANSLATION,
        ],
        priority=1,
    ),

    ModelProvider.VENICE: ModelConfig(
        provider=ModelProvider.VENICE,
        name="Venice AI",
        description="Privacy-sensitive tasks, uncensored content",
        api_base="https://api.venice.ai/api/v1",
        model_id="llama-3.3-70b",
        max_tokens=8192,
        cost_per_1k_tokens=0.0,  # Free tier available
        specializations=[
            TaskType.PRIVACY_SENSITIVE,
            TaskType.UNCENSORED,
        ],
        priority=1,
    ),

    ModelProvider.COPILOT: ModelConfig(
        provider=ModelProvider.COPILOT,
        name="Microsoft Copilot",
        description="Microsoft Office, enterprise workflows",
        api_base="https://api.github.com/copilot",
        model_id="copilot",
        max_tokens=8192,
        supports_function_calling=True,
        cost_per_1k_tokens=0.01,
        specializations=[
            TaskType.OFFICE_INTEGRATION,
            TaskType.ENTERPRISE,
        ],
        priority=2,
    ),

    ModelProvider.MANUS: ModelConfig(
        provider=ModelProvider.MANUS,
        name="Manus AI",
        description="Autonomous multi-step tasks, web automation",
        api_base="https://api.manus.ai/v1",
        model_id="manus-1",
        max_tokens=16384,
        supports_function_calling=True,
        cost_per_1k_tokens=0.015,
        specializations=[
            TaskType.WEB_AUTOMATION,
            TaskType.MULTI_STEP_TASK,
        ],
        priority=1,
    ),

    ModelProvider.CLAUDE: ModelConfig(
        provider=ModelProvider.CLAUDE,
        name="Claude (Orchestrator)",
        description="Analysis, long documents, orchestration, complex reasoning",
        api_base="https://api.anthropic.com/v1",
        model_id="claude-sonnet-4-20250514",
        max_tokens=200000,
        supports_vision=True,
        supports_function_calling=True,
        cost_per_1k_tokens=0.003,
        specializations=[
            TaskType.LONG_DOCUMENT,
            TaskType.COMPLEX_REASONING,
            TaskType.ANALYSIS,
            TaskType.ORCHESTRATION,
        ],
        priority=1,
    ),
}


# Task to Model Mapping (for quick lookup)
TASK_MODEL_MAP: dict[TaskType, list[ModelProvider]] = {}

def _build_task_model_map():
    """Build reverse mapping from tasks to models."""
    for provider, config in MODELS.items():
        for task in config.specializations:
            if task not in TASK_MODEL_MAP:
                TASK_MODEL_MAP[task] = []
            TASK_MODEL_MAP[task].append(provider)

    # Sort by priority
    for task in TASK_MODEL_MAP:
        TASK_MODEL_MAP[task].sort(
            key=lambda p: MODELS[p].priority
        )

_build_task_model_map()


# Keywords for task detection
TASK_KEYWORDS: dict[TaskType, list[str]] = {
    TaskType.CREATIVE_WRITING: [
        "write", "story", "poem", "creative", "fiction", "narrative",
        "اكتب", "قصة", "شعر", "إبداعي"
    ],
    TaskType.BRAINSTORMING: [
        "brainstorm", "ideas", "suggest", "think of", "come up with",
        "أفكار", "اقتراحات", "فكر"
    ],
    TaskType.CODE_GENERATION: [
        "code", "program", "function", "class", "implement", "develop",
        "python", "javascript", "typescript", "rust", "go",
        "كود", "برمجة", "دالة"
    ],
    TaskType.CODE_REVIEW: [
        "review", "check code", "improve code", "refactor",
        "راجع", "حسن الكود"
    ],
    TaskType.DEBUGGING: [
        "debug", "fix", "error", "bug", "issue", "problem",
        "خطأ", "مشكلة", "إصلاح"
    ],
    TaskType.ALGORITHMS: [
        "algorithm", "data structure", "complexity", "optimize",
        "خوارزمية", "هيكل بيانات"
    ],
    TaskType.RESEARCH: [
        "research", "find information", "look up", "investigate",
        "ابحث", "معلومات", "استقصاء"
    ],
    TaskType.FACT_CHECKING: [
        "fact check", "verify", "is it true", "accurate",
        "تحقق", "صحيح", "دقيق"
    ],
    TaskType.CURRENT_EVENTS: [
        "news", "today", "recent", "latest", "current",
        "أخبار", "اليوم", "حديث", "جديد"
    ],
    TaskType.IMAGE_ANALYSIS: [
        "image", "picture", "photo", "analyze image", "what's in",
        "صورة", "حلل الصورة"
    ],
    TaskType.ARABIC_CONTENT: [
        "arabic", "عربي", "بالعربي", "العربية"
    ],
    TaskType.CHINESE_CONTENT: [
        "chinese", "中文", "汉语", "صيني"
    ],
    TaskType.TRANSLATION: [
        "translate", "translation", "ترجم", "ترجمة"
    ],
    TaskType.LONG_DOCUMENT: [
        "document", "pdf", "long text", "analyze document",
        "مستند", "وثيقة", "ملف"
    ],
    TaskType.COMPLEX_REASONING: [
        "analyze", "complex", "reasoning", "think through",
        "تحليل", "معقد", "استنتاج"
    ],
    TaskType.PRIVACY_SENSITIVE: [
        "private", "confidential", "sensitive", "secret",
        "خاص", "سري", "حساس"
    ],
    TaskType.OFFICE_INTEGRATION: [
        "excel", "word", "powerpoint", "outlook", "microsoft",
        "إكسل", "وورد"
    ],
    TaskType.WEB_AUTOMATION: [
        "automate", "browser", "web scrape", "automation",
        "أتمتة", "متصفح"
    ],
    TaskType.MULTI_STEP_TASK: [
        "multi-step", "workflow", "process", "sequence",
        "خطوات", "عملية"
    ],
}
