from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    LLM_MODEL: str = "deepseek-r1:1.5b"
    EMBEDDING_MODEL: str = "nomic-embed-text"

    # RAG
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    TOP_K: int = 5

    # ChromaDB
    CHROMA_PERSIST_DIR: str = "./chroma_data"

    # API
    BACKEND_PORT: int = 8000
    FRONTEND_URL: str = "http://localhost:5173"

    # Paths
    PDF_DIR: str = str(Path(__file__).parent.parent / "data" / "pdfs")

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
