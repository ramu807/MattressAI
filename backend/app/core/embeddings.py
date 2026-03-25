import httpx
from app.config import settings


async def embed_texts(texts: list[str]) -> list[list[float]]:
    """Generate embeddings for a list of texts using Ollama's embedding API."""
    embeddings: list[list[float]] = []

    async with httpx.AsyncClient(timeout=120.0) as client:
        # Process in batches of 32 to avoid overloading
        batch_size = 32
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            response = await client.post(
                f"{settings.OLLAMA_BASE_URL}/api/embed",
                json={
                    "model": settings.EMBEDDING_MODEL,
                    "input": batch,
                },
            )
            response.raise_for_status()
            data = response.json()
            embeddings.extend(data["embeddings"])

    return embeddings


async def embed_single(text: str) -> list[float]:
    """Generate embedding for a single text."""
    result = await embed_texts([text])
    return result[0]
