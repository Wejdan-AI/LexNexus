"""
WejdanAI API
=============
FastAPI server for the multi-model RAG system.
"""

import os
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from ..config.models import ModelProvider, TaskType
from ..core import RAGEngine, get_engine, get_router


# Request/Response Models
class ChatRequest(BaseModel):
    """Chat completion request."""
    message: str = Field(..., description="User message")
    use_rag: bool = Field(True, description="Whether to use RAG retrieval")
    max_docs: int = Field(5, description="Maximum documents to retrieve")
    prefer_cost: bool = Field(False, description="Optimize for cost")
    prefer_quality: bool = Field(False, description="Optimize for quality")
    prefer_privacy: bool = Field(False, description="Optimize for privacy")
    force_model: Optional[str] = Field(None, description="Force specific model")
    system_prompt: Optional[str] = Field(None, description="Custom system prompt")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context")


class ChatResponse(BaseModel):
    """Chat completion response."""
    answer: str
    model_used: str
    model_name: str
    confidence: float
    reasoning: str
    citations: list[str] = []
    documents_used: int = 0
    usage: dict = {}
    latency_ms: float = 0.0


class RouteRequest(BaseModel):
    """Route analysis request."""
    message: str
    include_explanation: bool = True


class RouteResponse(BaseModel):
    """Route analysis response."""
    model: str
    model_name: str
    confidence: float
    reasoning: str
    detected_tasks: list[str]
    fallbacks: list[str]
    explanation: Optional[str] = None


class ModelInfo(BaseModel):
    """Model information."""
    id: str
    name: str
    description: str
    specializations: list[str]
    supports_vision: bool
    supports_streaming: bool
    enabled: bool


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    models_available: int


# Global engine instance
engine: Optional[RAGEngine] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    global engine
    engine = get_engine()
    yield
    if engine:
        await engine.close()


# Create FastAPI app
app = FastAPI(
    title="WejdanAI",
    description="Multi-Model RAG System with Intelligent Routing",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    from ..config.models import MODELS
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        models_available=len([m for m in MODELS.values() if m.enabled]),
    )


@app.get("/models", response_model=list[ModelInfo])
async def list_models():
    """List all available models."""
    from ..config.models import MODELS

    return [
        ModelInfo(
            id=provider.value,
            name=config.name,
            description=config.description,
            specializations=[t.value for t in config.specializations],
            supports_vision=config.supports_vision,
            supports_streaming=config.supports_streaming,
            enabled=config.enabled,
        )
        for provider, config in MODELS.items()
    ]


@app.post("/route", response_model=RouteResponse)
async def analyze_route(request: RouteRequest):
    """Analyze which model would be used for a message."""
    router = get_router()
    decision = router.route(request.message)

    from ..config.models import MODELS

    response = RouteResponse(
        model=decision.primary_model.value,
        model_name=decision.model_config.name,
        confidence=decision.confidence,
        reasoning=decision.reasoning,
        detected_tasks=[t.value for t in decision.detected_tasks],
        fallbacks=[m.value for m in decision.fallback_models],
    )

    if request.include_explanation:
        response.explanation = router.explain_routing(decision)

    return response


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a chat message and get a response."""
    global engine

    if not engine:
        raise HTTPException(status_code=500, detail="Engine not initialized")

    # Build preferences
    preferences = {}
    if request.prefer_cost:
        preferences["prefer_cost"] = True
    if request.prefer_quality:
        preferences["prefer_quality"] = True
    if request.prefer_privacy:
        preferences["prefer_privacy"] = True

    # Parse force model
    force_model = None
    if request.force_model:
        try:
            force_model = ModelProvider(request.force_model)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid model: {request.force_model}",
            )

    try:
        # Query the RAG engine
        result = await engine.query(
            question=request.message,
            use_rag=request.use_rag,
            max_docs=request.max_docs,
            preferences=preferences if preferences else None,
            force_model=force_model,
            system_prompt=request.system_prompt,
        )

        from ..config.models import MODELS

        return ChatResponse(
            answer=result.answer,
            model_used=result.model_used.value,
            model_name=MODELS[result.model_used].name,
            confidence=result.routing_decision.confidence,
            reasoning=result.routing_decision.reasoning,
            citations=result.completion.citations,
            documents_used=len(result.documents),
            usage=result.completion.usage,
            latency_ms=result.completion.latency_ms,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Stream a chat response."""
    from fastapi.responses import StreamingResponse

    global engine

    if not engine:
        raise HTTPException(status_code=500, detail="Engine not initialized")

    # Build preferences
    preferences = {}
    if request.prefer_cost:
        preferences["prefer_cost"] = True
    if request.prefer_quality:
        preferences["prefer_quality"] = True
    if request.prefer_privacy:
        preferences["prefer_privacy"] = True

    # Route to model
    router = get_router()
    decision = router.route(
        request.message,
        preferences=preferences if preferences else None,
    )

    # Get provider
    provider = engine._get_provider(decision.primary_model)
    if not provider:
        raise HTTPException(
            status_code=500,
            detail=f"Provider not available: {decision.primary_model.value}",
        )

    async def generate():
        from ..providers import Message

        messages = [Message(role="user", content=request.message)]

        try:
            async for chunk in provider.stream(
                messages=messages,
                system_prompt=request.system_prompt,
            ):
                yield f"data: {chunk}\n\n"
        except Exception as e:
            yield f"data: [ERROR] {str(e)}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
    )


@app.post("/documents/search")
async def search_documents(
    query: str,
    max_docs: int = 5,
):
    """Search for documents in the knowledge base."""
    global engine

    if not engine:
        raise HTTPException(status_code=500, detail="Engine not initialized")

    documents = await engine.retrieve(query, max_docs=max_docs)

    return {
        "query": query,
        "count": len(documents),
        "documents": [
            {
                "id": doc.id,
                "title": doc.title,
                "content": doc.content[:500] + "..." if len(doc.content) > 500 else doc.content,
                "source": doc.source,
                "score": doc.score,
            }
            for doc in documents
        ],
    }


@app.get("/tasks")
async def list_task_types():
    """List all task types and their associated models."""
    from ..config.models import MODELS, TASK_MODEL_MAP

    return {
        task.value: {
            "models": [m.value for m in models],
            "primary_model": MODELS[models[0]].name if models else None,
        }
        for task, models in TASK_MODEL_MAP.items()
    }


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    return app


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
