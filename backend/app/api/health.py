import httpx
from fastapi import APIRouter
from app.config import settings
from app.core import vector_store

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
async def health_check():
    """Check system health: Ollama connectivity, ChromaDB status, model availability."""
    # Check Ollama
    ollama_status = "disconnected"
    available_models: list[str] = []
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
            if resp.status_code == 200:
                ollama_status = "connected"
                models_data = resp.json().get("models", [])
                available_models = [m["name"] for m in models_data]
    except Exception:
        ollama_status = "disconnected"

    # Check required models
    llm_ready = any(settings.LLM_MODEL in m for m in available_models)
    embedding_ready = any(settings.EMBEDDING_MODEL in m for m in available_models)

    # Check vector store (FAISS)
    chroma_stats = vector_store.get_stats()

    return {
        "status": "healthy" if ollama_status == "connected" else "degraded",
        "ollama": {
            "status": ollama_status,
            "url": settings.OLLAMA_BASE_URL,
            "llm_model": settings.LLM_MODEL,
            "llm_ready": llm_ready,
            "embedding_model": settings.EMBEDDING_MODEL,
            "embedding_ready": embedding_ready,
        },
        "chromadb": chroma_stats,
        "config": {
            "chunk_size": settings.CHUNK_SIZE,
            "chunk_overlap": settings.CHUNK_OVERLAP,
            "top_k": settings.TOP_K,
        },
    }
