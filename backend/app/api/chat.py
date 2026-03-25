import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.rag_pipeline import pipeline
from app.core.chat_store import add_message

router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    query: str
    chat_history: list[dict] = []
    stream: bool = True
    session_id: str | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[dict]
    query: str


async def _stream_and_save(question, chat_history, session_id):
    """Wrap query_stream to accumulate the full response and save to session."""
    full_content = ""
    sources = []

    async for event_str in pipeline.query_stream(
        question=question,
        chat_history=chat_history,
    ):
        yield event_str

        # Parse the SSE event to accumulate content
        try:
            line = event_str.strip()
            if line.startswith("data: "):
                data = json.loads(line[6:])
                if data.get("type") == "token":
                    full_content += data["data"]
                elif data.get("type") == "sources":
                    sources = data["data"]
        except (json.JSONDecodeError, KeyError):
            pass

    # Save assistant message after streaming completes
    if session_id:
        add_message(session_id, "assistant", full_content, sources)


@router.post("/chat")
async def chat(request: ChatRequest):
    """Query the RAG pipeline. Supports streaming (SSE) and non-streaming modes."""
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # Save user message to session if session_id provided
    if request.session_id:
        add_message(request.session_id, "user", request.query)

    if request.stream:
        return StreamingResponse(
            _stream_and_save(
                question=request.query,
                chat_history=request.chat_history,
                session_id=request.session_id,
            ),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )
    else:
        result = await pipeline.query(
            question=request.query,
            chat_history=request.chat_history,
        )
        if request.session_id:
            add_message(request.session_id, "assistant", result.answer, result.sources)
        return ChatResponse(
            answer=result.answer,
            sources=result.sources,
            query=result.query,
        )
