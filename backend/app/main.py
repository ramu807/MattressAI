from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.chat import router as chat_router
from app.api.documents import router as documents_router
from app.api.health import router as health_router
from app.api.sessions import router as sessions_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize services on startup."""
    # Initialize ChromaDB collection on startup
    from app.core import vector_store
    vector_store.get_collection()
    print(f"ChromaDB initialized. Documents: {vector_store.get_stats()['document_count']}")
    print(f"Ollama URL: {settings.OLLAMA_BASE_URL}")
    print(f"LLM Model: {settings.LLM_MODEL}")
    print(f"Embedding Model: {settings.EMBEDDING_MODEL}")
    yield


app = FastAPI(
    title="MattressAI RAG API",
    description="Professional RAG system for mattress knowledge using local LLM (DeepSeek via Ollama)",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(chat_router)
app.include_router(documents_router)
app.include_router(health_router)
app.include_router(sessions_router)


@app.get("/")
async def root():
    return {
        "name": "MattressAI RAG API",
        "version": "1.0.0",
        "docs": "/docs",
    }
