from dataclasses import dataclass
from app.core.embeddings import embed_single
from app.core import vector_store


@dataclass
class RetrievedChunk:
    text: str
    source: str
    page: int
    relevance_score: float
    chunk_index: int = 0


async def retrieve(query: str, top_k: int | None = None) -> list[RetrievedChunk]:
    """Retrieve the most relevant chunks for a query."""
    # Embed the query
    query_embedding = await embed_single(query)

    # Search ChromaDB
    results = vector_store.query(query_embedding, top_k=top_k)

    chunks: list[RetrievedChunk] = []
    if results and results.get("documents") and results["documents"][0]:
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for doc, meta, distance in zip(documents, metadatas, distances):
            # ChromaDB cosine distance: 0 = identical, 2 = opposite
            # Convert to similarity score (0-1)
            relevance = max(0.0, 1.0 - (distance / 2.0))
            chunks.append(RetrievedChunk(
                text=doc,
                source=meta.get("source", "unknown"),
                page=meta.get("page", 0),
                relevance_score=round(relevance, 4),
                chunk_index=meta.get("chunk_index", 0),
            ))

    return chunks
