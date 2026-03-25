import json
import faiss
import numpy as np
from pathlib import Path
from app.config import settings

COLLECTION_NAME = "mattress_docs"

# In-memory state
_index: faiss.IndexFlatIP | None = None
_documents: list[str] = []
_metadatas: list[dict] = []


def _store_path() -> Path:
    p = Path(settings.CHROMA_PERSIST_DIR)
    p.mkdir(parents=True, exist_ok=True)
    return p


def _save():
    """Persist index and metadata to disk."""
    path = _store_path()
    if _index is not None and _index.ntotal > 0:
        faiss.write_index(_index, str(path / "index.faiss"))
        with open(path / "metadata.json", "w", encoding="utf-8") as f:
            json.dump({"documents": _documents, "metadatas": _metadatas}, f)


def _load():
    """Load index and metadata from disk."""
    global _index, _documents, _metadatas
    path = _store_path()
    index_file = path / "index.faiss"
    meta_file = path / "metadata.json"

    if index_file.exists() and meta_file.exists():
        _index = faiss.read_index(str(index_file))
        with open(meta_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            _documents = data["documents"]
            _metadatas = data["metadatas"]
    else:
        _index = None
        _documents = []
        _metadatas = []


def get_collection():
    """Ensure index is loaded."""
    global _index
    if _index is None:
        _load()


def add_documents(
    ids: list[str],
    documents: list[str],
    embeddings: list[list[float]],
    metadatas: list[dict],
) -> None:
    """Add documents with embeddings to the vector store."""
    global _index, _documents, _metadatas

    vectors = np.array(embeddings, dtype="float32")
    # Normalize for cosine similarity (inner product on unit vectors = cosine sim)
    faiss.normalize_L2(vectors)

    dim = vectors.shape[1]
    if _index is None:
        _index = faiss.IndexFlatIP(dim)
        _documents = []
        _metadatas = []

    _index.add(vectors)
    _documents.extend(documents)
    _metadatas.extend(metadatas)
    _save()


def query(embedding: list[float], top_k: int | None = None) -> dict:
    """Query the vector store for similar documents."""
    if top_k is None:
        top_k = settings.TOP_K

    get_collection()
    if _index is None or _index.ntotal == 0:
        return {"documents": [[]], "metadatas": [[]], "distances": [[]]}

    vec = np.array([embedding], dtype="float32")
    faiss.normalize_L2(vec)

    k = min(top_k, _index.ntotal)
    scores, indices = _index.search(vec, k)

    docs = []
    metas = []
    dists = []
    for i, idx in enumerate(indices[0]):
        if idx < 0:
            continue
        docs.append(_documents[idx])
        metas.append(_metadatas[idx])
        # Convert inner product score (0-1 for normalized) to distance-like (0=best)
        dists.append(float(1.0 - scores[0][i]))

    return {"documents": [docs], "metadatas": [metas], "distances": [dists]}


def get_stats() -> dict:
    """Get collection statistics."""
    get_collection()
    return {
        "collection": COLLECTION_NAME,
        "document_count": _index.ntotal if _index else 0,
    }


def reset_collection() -> None:
    """Delete and recreate the collection."""
    global _index, _documents, _metadatas
    _index = None
    _documents = []
    _metadatas = []
    path = _store_path()
    for f in [path / "index.faiss", path / "metadata.json"]:
        if f.exists():
            f.unlink()
