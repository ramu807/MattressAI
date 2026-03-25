import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.chunker import chunk_text, chunk_pages
from app.core.pdf_loader import PageContent


def test_chunk_text_basic():
    text = "This is the first paragraph.\n\nThis is the second paragraph.\n\nThis is the third paragraph."
    chunks = chunk_text(text, chunk_size=60, chunk_overlap=10)
    assert len(chunks) > 0
    for chunk in chunks:
        assert len(chunk) >= 20


def test_chunk_text_respects_size():
    text = " ".join(["word"] * 500)
    chunks = chunk_text(text, chunk_size=100, chunk_overlap=20)
    assert len(chunks) > 1


def test_chunk_pages():
    pages = [
        PageContent(text="This is a test page with enough content to create chunks. " * 10,
                     metadata={"source": "test.pdf", "page": 1}),
        PageContent(text="Another page with different content about mattresses. " * 10,
                     metadata={"source": "test.pdf", "page": 2}),
    ]
    chunks = chunk_pages(pages, chunk_size=100, chunk_overlap=20)
    assert len(chunks) > 0
    for chunk in chunks:
        assert "source" in chunk.metadata
        assert "page" in chunk.metadata
        assert "chunk_index" in chunk.metadata


def test_empty_text():
    chunks = chunk_text("", chunk_size=500, chunk_overlap=50)
    assert len(chunks) == 0


if __name__ == "__main__":
    test_chunk_text_basic()
    test_chunk_text_respects_size()
    test_chunk_pages()
    test_empty_text()
    print("All chunker tests passed!")
