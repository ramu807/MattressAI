from app.core.retriever import RetrievedChunk

SYSTEM_PROMPT = """You are MattressAI, a professional mattress expert assistant. Your role is to provide accurate, helpful information about mattresses based on the provided context.

RULES:
1. Answer questions using ONLY the information from the provided context below.
2. Always cite your sources using the format [Source: filename, Page X].
3. If the context does not contain enough information to answer the question, clearly state: "I don't have enough information in my knowledge base to answer that question fully."
4. Be professional, concise, and helpful.
5. If the user asks about topics unrelated to mattresses, politely redirect them.
6. Structure your answers with clear formatting when appropriate (bullet points, headings).
"""


def build_context(chunks: list[RetrievedChunk]) -> str:
    """Format retrieved chunks into a context string."""
    if not chunks:
        return "No relevant context found."

    context_parts: list[str] = []
    for i, chunk in enumerate(chunks, 1):
        context_parts.append(
            f"[Context {i}] (Source: {chunk.source}, Page {chunk.page}, "
            f"Relevance: {chunk.relevance_score:.0%})\n{chunk.text}"
        )

    return "\n\n---\n\n".join(context_parts)


def build_messages(
    query: str,
    chunks: list[RetrievedChunk],
    chat_history: list[dict] | None = None,
) -> list[dict]:
    """Build the full message list for the LLM."""
    messages: list[dict] = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    # Add chat history (last 3 exchanges for context)
    if chat_history:
        for msg in chat_history[-6:]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"],
            })

    # Build user message with context
    context = build_context(chunks)
    user_message = f"""Based on the following context, please answer my question.

CONTEXT:
{context}

QUESTION: {query}"""

    messages.append({"role": "user", "content": user_message})

    return messages
