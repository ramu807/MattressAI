import json
import time
from dataclasses import dataclass
from collections.abc import AsyncGenerator
from app.core.embeddings import embed_single
from app.core import vector_store
from app.core.retriever import RetrievedChunk
from app.core.prompt import build_messages
from app.core.generator import generate


@dataclass
class RAGResponse:
    answer: str
    sources: list[dict]
    query: str


def _sse(event_type: str, data) -> str:
    return f"data: {json.dumps({'type': event_type, 'data': data})}\n\n"


def _step_event(step: str, status: str, duration_ms: int | None = None, detail: dict | None = None) -> str:
    payload: dict = {"step": step, "status": status}
    if duration_ms is not None:
        payload["duration_ms"] = duration_ms
    if detail:
        payload.update(detail)
    return _sse("step", payload)


class RAGPipeline:
    """Orchestrates the full RAG pipeline: Retrieve → Prompt → Generate."""

    async def query(
        self,
        question: str,
        chat_history: list[dict] | None = None,
        top_k: int | None = None,
    ) -> RAGResponse:
        """Run a full RAG query and return the complete response."""
        query_embedding = await embed_single(question)
        results = vector_store.query(query_embedding, top_k=top_k)
        chunks = self._parse_results(results)
        messages = build_messages(question, chunks, chat_history)

        full_answer = ""
        async for token in generate(messages, stream=True):
            full_answer += token

        sources = self._build_sources(chunks)
        return RAGResponse(answer=full_answer, sources=sources, query=question)

    async def query_stream(
        self,
        question: str,
        chat_history: list[dict] | None = None,
        top_k: int | None = None,
    ) -> AsyncGenerator[str, None]:
        """Run a RAG query with streaming response (SSE format) and pipeline step events."""

        # Step 1: Embedding
        yield _step_event("embedding", "active")
        t0 = time.perf_counter()
        query_embedding = await embed_single(question)
        t1 = time.perf_counter()
        yield _step_event("embedding", "done", duration_ms=round((t1 - t0) * 1000))

        # Step 2: Vector DB retrieval
        yield _step_event("retrieval", "active")
        t0 = time.perf_counter()
        results = vector_store.query(query_embedding, top_k=top_k)
        chunks = self._parse_results(results)
        t1 = time.perf_counter()
        yield _step_event("retrieval", "done", duration_ms=round((t1 - t0) * 1000), detail={"chunks_found": len(chunks)})

        # Send sources
        sources = self._build_sources(chunks)
        yield _sse("sources", sources)

        # Step 3: Build prompt
        messages = build_messages(question, chunks, chat_history)

        # Step 4: LLM generation
        yield _step_event("generation", "active")
        t0 = time.perf_counter()
        token_count = 0
        async for token in generate(messages, stream=True):
            token_count += 1
            yield _sse("token", token)
        t1 = time.perf_counter()
        yield _step_event("generation", "done", duration_ms=round((t1 - t0) * 1000), detail={"tokens": token_count})

        # Done
        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    @staticmethod
    def _parse_results(results: dict) -> list[RetrievedChunk]:
        chunks: list[RetrievedChunk] = []
        if results and results.get("documents") and results["documents"][0]:
            documents = results["documents"][0]
            metadatas = results["metadatas"][0]
            distances = results["distances"][0]
            for doc, meta, distance in zip(documents, metadatas, distances):
                relevance = max(0.0, 1.0 - (distance / 2.0))
                chunks.append(RetrievedChunk(
                    text=doc,
                    source=meta.get("source", "unknown"),
                    page=meta.get("page", 0),
                    relevance_score=round(relevance, 4),
                    chunk_index=meta.get("chunk_index", 0),
                ))
        return chunks

    @staticmethod
    def _build_sources(chunks: list[RetrievedChunk]) -> list[dict]:
        return [
            {
                "text": c.text[:200] + ("..." if len(c.text) > 200 else ""),
                "source": c.source,
                "page": c.page,
                "relevance_score": c.relevance_score,
            }
            for c in chunks
        ]


# Singleton instance
pipeline = RAGPipeline()
