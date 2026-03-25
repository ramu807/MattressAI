"""
Standalone ingestion script.
Run: python -m ingest
From the backend/ directory.
"""
import asyncio
import uuid
import sys
from pathlib import Path

# Ensure the backend directory is in the path
sys.path.insert(0, str(Path(__file__).parent))

from app.config import settings
from app.core.pdf_loader import load_pdfs_from_directory
from app.core.chunker import chunk_pages
from app.core.embeddings import embed_texts
from app.core import vector_store


async def ingest():
    pdf_dir = settings.PDF_DIR
    print(f"📂 Loading PDFs from: {pdf_dir}")

    pages = load_pdfs_from_directory(pdf_dir)
    if not pages:
        print("❌ No pages extracted from PDFs. Check that PDF files exist in data/pdfs/")
        return

    print(f"📄 Extracted {len(pages)} pages from PDFs")

    # Chunk
    chunks = chunk_pages(pages, settings.CHUNK_SIZE, settings.CHUNK_OVERLAP)
    print(f"🔪 Created {len(chunks)} chunks (size={settings.CHUNK_SIZE}, overlap={settings.CHUNK_OVERLAP})")

    # Embed
    print(f"🧠 Generating embeddings with {settings.EMBEDDING_MODEL}...")
    texts = [c.text for c in chunks]
    embeddings = await embed_texts(texts)
    print(f"✅ Generated {len(embeddings)} embeddings (dim={len(embeddings[0])})")

    # Store
    print("💾 Storing in ChromaDB...")
    vector_store.reset_collection()
    ids = [str(uuid.uuid4()) for _ in chunks]
    metadatas = [c.metadata for c in chunks]
    vector_store.add_documents(ids, texts, embeddings, metadatas)

    stats = vector_store.get_stats()
    print(f"✅ Ingestion complete! {stats['document_count']} chunks stored in collection '{stats['collection']}'")

    # Print summary per source
    sources = {}
    for chunk in chunks:
        src = chunk.metadata.get("source", "unknown")
        sources[src] = sources.get(src, 0) + 1
    print("\n📊 Summary:")
    for src, count in sources.items():
        print(f"   {src}: {count} chunks")


if __name__ == "__main__":
    asyncio.run(ingest())
