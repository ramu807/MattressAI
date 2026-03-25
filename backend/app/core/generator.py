import json
from collections.abc import AsyncGenerator
import httpx
from app.config import settings


async def generate(messages: list[dict], stream: bool = True) -> AsyncGenerator[str, None]:
    """Generate a response from Ollama, yielding tokens as they arrive."""
    async with httpx.AsyncClient(timeout=300.0) as client:
        async with client.stream(
            "POST",
            f"{settings.OLLAMA_BASE_URL}/api/chat",
            json={
                "model": settings.LLM_MODEL,
                "messages": messages,
                "stream": stream,
            },
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if not line:
                    continue
                data = json.loads(line)
                if "message" in data and "content" in data["message"]:
                    yield data["message"]["content"]
                if data.get("done", False):
                    break


async def generate_full(messages: list[dict]) -> str:
    """Generate a complete (non-streaming) response."""
    full_response = ""
    async for token in generate(messages, stream=True):
        full_response += token
    return full_response
