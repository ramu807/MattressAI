import { useState, useEffect } from 'react';
import { ChatSession } from '../types';
import { fetchSessions, deleteSession as apiDeleteSession } from '../services/api';

interface ChatHistoryProps {
  currentSessionId: string | null;
  onSelectSession: (sessionId: string) => void;
  onNewChat: () => void;
  refreshTrigger: number;
}

export default function ChatHistory({ currentSessionId, onSelectSession, onNewChat, refreshTrigger }: ChatHistoryProps) {
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [confirmDelete, setConfirmDelete] = useState<string | null>(null);

  const loadSessions = () => {
    fetchSessions().then(setSessions).catch(() => {});
  };

  useEffect(() => {
    loadSessions();
  }, [refreshTrigger]);

  const handleDelete = async (e: React.MouseEvent, sessionId: string) => {
    e.stopPropagation();
    if (confirmDelete === sessionId) {
      await apiDeleteSession(sessionId).catch(() => {});
      setConfirmDelete(null);
      loadSessions();
      if (currentSessionId === sessionId) {
        onNewChat();
      }
    } else {
      setConfirmDelete(sessionId);
      setTimeout(() => setConfirmDelete(null), 3000);
    }
  };

  const formatTime = (iso: string) => {
    const d = new Date(iso);
    const now = new Date();
    const diffMs = now.getTime() - d.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    const diffHrs = Math.floor(diffMins / 60);
    if (diffHrs < 24) return `${diffHrs}h ago`;
    const diffDays = Math.floor(diffHrs / 24);
    if (diffDays < 7) return `${diffDays}d ago`;
    return d.toLocaleDateString();
  };

  return (
    <section>
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-xs font-medium text-dark-400 uppercase tracking-wider">Chat History</h3>
        <button
          onClick={onNewChat}
          className="flex items-center gap-1 text-xs text-primary-400 hover:text-primary-300 transition-colors"
        >
          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          New
        </button>
      </div>

      {sessions.length === 0 ? (
        <div className="text-xs text-dark-500 text-center py-4">
          No conversations yet
        </div>
      ) : (
        <div className="space-y-1 max-h-64 overflow-y-auto">
          {sessions.map(session => (
            <div
              key={session.id}
              onClick={() => onSelectSession(session.id)}
              className={`group flex items-start gap-2 p-2 rounded-lg cursor-pointer transition-all ${
                currentSessionId === session.id
                  ? 'bg-primary-600/20 border border-primary-600/30'
                  : 'hover:bg-dark-800 border border-transparent'
              }`}
            >
              <svg className="w-4 h-4 text-dark-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
                  d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
              <div className="flex-1 min-w-0">
                <p className="text-sm text-dark-200 truncate">{session.title}</p>
                <div className="flex items-center gap-2 mt-0.5">
                  <span className="text-[10px] text-dark-500">{formatTime(session.updated_at)}</span>
                  <span className="text-[10px] text-dark-600">{session.message_count} msgs</span>
                </div>
              </div>
              <button
                onClick={(e) => handleDelete(e, session.id)}
                className={`flex-shrink-0 p-1 rounded opacity-0 group-hover:opacity-100 transition-opacity ${
                  confirmDelete === session.id
                    ? 'opacity-100 text-red-400 hover:text-red-300'
                    : 'text-dark-500 hover:text-dark-300'
                }`}
                title={confirmDelete === session.id ? 'Click again to confirm' : 'Delete'}
              >
                <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                    d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
