import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from app.config import settings


SESSIONS_DIR = Path(settings.PDF_DIR).parent / "chat_sessions"


def _ensure_dir():
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)


def _session_path(session_id: str) -> Path:
    # Sanitize to prevent path traversal
    safe_id = Path(session_id).name
    return SESSIONS_DIR / f"{safe_id}.json"


def create_session(title: str = "New Chat") -> dict:
    _ensure_dir()
    session_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    session = {
        "id": session_id,
        "title": title,
        "created_at": now,
        "updated_at": now,
        "messages": [],
    }
    _session_path(session_id).write_text(json.dumps(session, indent=2), encoding="utf-8")
    return session


def list_sessions() -> list[dict]:
    _ensure_dir()
    sessions = []
    for f in sorted(SESSIONS_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            sessions.append({
                "id": data["id"],
                "title": data["title"],
                "created_at": data["created_at"],
                "updated_at": data["updated_at"],
                "message_count": len(data["messages"]),
            })
        except (json.JSONDecodeError, KeyError):
            continue
    return sessions


def get_session(session_id: str) -> dict | None:
    _ensure_dir()
    path = _session_path(session_id)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, KeyError):
        return None


def delete_session(session_id: str) -> bool:
    path = _session_path(session_id)
    if path.exists():
        path.unlink()
        return True
    return False


def add_message(session_id: str, role: str, content: str, sources: list[dict] | None = None) -> dict | None:
    session = get_session(session_id)
    if session is None:
        return None
    now = datetime.now(timezone.utc).isoformat()
    message = {
        "id": str(uuid.uuid4()),
        "role": role,
        "content": content,
        "sources": sources or [],
        "timestamp": now,
    }
    session["messages"].append(message)
    session["updated_at"] = now
    # Auto-title from first user message
    if role == "user" and len([m for m in session["messages"] if m["role"] == "user"]) == 1:
        session["title"] = content[:50] + ("..." if len(content) > 50 else "")
    _session_path(session_id).write_text(json.dumps(session, indent=2), encoding="utf-8")
    return message
