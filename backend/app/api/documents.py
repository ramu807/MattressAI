import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.config import settings
from app.core.pdf_loader import load_pdf, load_pdfs_from_directory
from app.core.chunker import chunk_pages
from app.core.embeddings import embed_texts
from app.core import vector_store

router = APIRouter(prefix="/api", tags=["documents"])


@router.get("/documents")
async def list_documents():
    """List ingested documents and statistics."""
    stats = vector_store.get_stats()
    pdf_dir = Path(settings.PDF_DIR)
    available_pdfs = [f.name for f in pdf_dir.glob("*.pdf")] if pdf_dir.exists() else []

    return {
        "ingested": stats,
        "available_pdfs": available_pdfs,
        "pdf_directory": str(pdf_dir),
    }


@router.post("/ingest")
async def ingest_documents():
    """Ingest all PDFs from the data/pdfs directory."""
    pdf_dir = Path(settings.PDF_DIR)
    if not pdf_dir.exists():
        raise HTTPException(status_code=404, detail=f"PDF directory not found: {pdf_dir}")

    pdf_files = list(pdf_dir.glob("*.pdf"))
    if not pdf_files:
        raise HTTPException(status_code=404, detail="No PDF files found in the data directory")

    # Reset collection for fresh ingestion
    vector_store.reset_collection()

    # Load and chunk PDFs
    pages = load_pdfs_from_directory(str(pdf_dir))
    chunks = chunk_pages(pages, settings.CHUNK_SIZE, settings.CHUNK_OVERLAP)

    if not chunks:
        raise HTTPException(status_code=400, detail="No text could be extracted from the PDFs")

    # Generate embeddings
    texts = [c.text for c in chunks]
    embeddings = await embed_texts(texts)

    # Store in ChromaDB
    ids = [str(uuid.uuid4()) for _ in chunks]
    metadatas = [c.metadata for c in chunks]
    vector_store.add_documents(ids, texts, embeddings, metadatas)

    return {
        "status": "success",
        "documents_processed": len(pdf_files),
        "chunks_created": len(chunks),
        "pdf_files": [f.name for f in pdf_files],
    }


@router.post("/upload")
async def upload_and_ingest(file: UploadFile = File(...)):
    """Upload a PDF file and ingest it."""
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    # Save file to PDF directory
    pdf_dir = Path(settings.PDF_DIR)
    pdf_dir.mkdir(parents=True, exist_ok=True)
    file_path = pdf_dir / file.filename
    content = await file.read()
    file_path.write_bytes(content)

    # Ingest the single file
    pages = load_pdf(str(file_path))
    chunks = chunk_pages(pages, settings.CHUNK_SIZE, settings.CHUNK_OVERLAP)

    if not chunks:
        raise HTTPException(status_code=400, detail="No text could be extracted from the PDF")

    texts = [c.text for c in chunks]
    embeddings = await embed_texts(texts)

    ids = [str(uuid.uuid4()) for _ in chunks]
    metadatas = [c.metadata for c in chunks]
    vector_store.add_documents(ids, texts, embeddings, metadatas)

    return {
        "status": "success",
        "filename": file.filename,
        "chunks_created": len(chunks),
    }
