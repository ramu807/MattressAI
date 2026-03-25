from fastapi import APIRouter, HTTPException

from app.core.chat_store import create_session, list_sessions, get_session, delete_session

router = APIRouter(prefix="/api", tags=["sessions"])


@router.get("/sessions")
async def get_sessions():
    return list_sessions()


@router.post("/sessions")
async def new_session():
    return create_session()


@router.get("/sessions/{session_id}")
async def get_session_detail(session_id: str):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.delete("/sessions/{session_id}")
async def remove_session(session_id: str):
    if not delete_session(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    return {"status": "deleted"}
