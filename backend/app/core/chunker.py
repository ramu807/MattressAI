from dataclasses import dataclass, field


@dataclass
class Chunk:
    text: str
    metadata: dict = field(default_factory=dict)


def _split_text(text: str, separators: list[str], chunk_size: int, chunk_overlap: int) -> list[str]:
    """Recursively split text using a hierarchy of separators."""
    if not text:
        return []

    separator = separators[0] if separators else ""
    remaining_separators = separators[1:] if len(separators) > 1 else []

    # Split by the current separator
    if separator:
        parts = text.split(separator)
    else:
        # Character-level splitting as last resort
        parts = list(text)

    chunks: list[str] = []
    current_chunk = ""

    for part in parts:
        # Add separator back (except for char-level splits)
        piece = part if not separator else (part + separator if part != parts[-1] else part)

        if len(current_chunk) + len(piece) <= chunk_size:
            current_chunk += piece
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())

            # If single piece exceeds chunk_size, try splitting with next separator
            if len(piece) > chunk_size and remaining_separators:
                sub_chunks = _split_text(piece, remaining_separators, chunk_size, chunk_overlap)
                chunks.extend(sub_chunks)
                current_chunk = ""
            else:
                current_chunk = piece

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


def _apply_overlap(chunks: list[str], overlap: int) -> list[str]:
    """Add overlap between consecutive chunks."""
    if overlap <= 0 or len(chunks) <= 1:
        return chunks

    overlapped: list[str] = [chunks[0]]
    for i in range(1, len(chunks)):
        prev_text = chunks[i - 1]
        overlap_text = prev_text[-overlap:] if len(prev_text) > overlap else prev_text
        # Find a clean break point in overlap (word boundary)
        space_idx = overlap_text.find(" ")
        if space_idx > 0:
            overlap_text = overlap_text[space_idx + 1:]
        overlapped.append(overlap_text + " " + chunks[i])

    return overlapped


def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list[str]:
    """Split text into overlapping chunks using recursive character splitting."""
    separators = ["\n\n", "\n", ". ", " "]
    chunks = _split_text(text, separators, chunk_size, chunk_overlap)
    chunks = _apply_overlap(chunks, chunk_overlap)
    # Filter out very small chunks
    return [c for c in chunks if len(c) >= 20]


def chunk_pages(pages: list, chunk_size: int = 500, chunk_overlap: int = 50) -> list[Chunk]:
    """Chunk a list of PageContent objects into Chunk objects with metadata."""
    all_chunks: list[Chunk] = []
    for page in pages:
        text_chunks = chunk_text(page.text, chunk_size, chunk_overlap)
        for idx, text in enumerate(text_chunks):
            all_chunks.append(Chunk(
                text=text,
                metadata={
                    **page.metadata,
                    "chunk_index": idx,
                    "chunk_total": len(text_chunks),
                }
            ))

    return all_chunks
