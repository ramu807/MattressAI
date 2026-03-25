import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.prompt import build_messages, build_context
from app.core.retriever import RetrievedChunk


def test_build_context():
    chunks = [
        RetrievedChunk(text="Memory foam is great for back pain.", source="guide.pdf", page=3, relevance_score=0.92),
        RetrievedChunk(text="Latex mattresses last 12-20 years.", source="care.pdf", page=5, relevance_score=0.85),
    ]
    context = build_context(chunks)
    assert "Memory foam" in context
    assert "guide.pdf" in context
    assert "Page 3" in context
    assert "92%" in context


def test_build_messages():
    chunks = [
        RetrievedChunk(text="Test content", source="test.pdf", page=1, relevance_score=0.90),
    ]
    messages = build_messages("What is the best mattress?", chunks)
    assert messages[0]["role"] == "system"
    assert messages[-1]["role"] == "user"
    assert "What is the best mattress?" in messages[-1]["content"]
    assert "Test content" in messages[-1]["content"]


def test_build_messages_with_history():
    chunks = [
        RetrievedChunk(text="Content", source="test.pdf", page=1, relevance_score=0.90),
    ]
    history = [
        {"role": "user", "content": "Hi"},
        {"role": "assistant", "content": "Hello!"},
    ]
    messages = build_messages("Follow up", chunks, chat_history=history)
    # system + 2 history + 1 user = 4
    assert len(messages) == 4
    assert messages[1]["content"] == "Hi"
    assert messages[2]["content"] == "Hello!"


def test_empty_chunks():
    context = build_context([])
    assert "No relevant context" in context


if __name__ == "__main__":
    test_build_context()
    test_build_messages()
    test_build_messages_with_history()
    test_empty_chunks()
    print("All prompt tests passed!")
