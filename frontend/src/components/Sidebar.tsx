import { useState, useEffect } from 'react';
import { DocumentInfo, HealthStatus } from '../types';
import { fetchDocuments, fetchHealth, ingestDocuments } from '../services/api';
import ChatHistory from './ChatHistory';

interface SidebarProps {
  open: boolean;
  onClose: () => void;
  currentSessionId: string | null;
  onSelectSession: (sessionId: string) => void;
  onNewChat: () => void;
  sessionRefresh: number;
}

export default function Sidebar({ open, onClose, currentSessionId, onSelectSession, onNewChat, sessionRefresh }: SidebarProps) {
  const [docs, setDocs] = useState<DocumentInfo | null>(null);
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [ingesting, setIngesting] = useState(false);
  const [ingestResult, setIngestResult] = useState<string | null>(null);

  const refreshData = () => {
    fetchDocuments().then(setDocs).catch(() => {});
    fetchHealth().then(setHealth).catch(() => {});
  };

  useEffect(() => {
    refreshData();
  }, []);

  const handleIngest = async () => {
    setIngesting(true);
    setIngestResult(null);
    try {
      const result = await ingestDocuments();
      setIngestResult(`Ingested ${result.documents_processed} PDFs → ${result.chunks_created} chunks`);
      refreshData();
    } catch (err) {
      setIngestResult(`Error: ${err instanceof Error ? err.message : 'Failed'}`);
    } finally {
      setIngesting(false);
    }
  };

  const isConnected = health?.ollama?.status === 'connected';

  return (
    <>
      {/* Overlay for mobile */}
      {open && (
        <div className="fixed inset-0 bg-black/50 z-20 lg:hidden" onClick={onClose} />
      )}

      <aside className={`
        fixed lg:static inset-y-0 left-0 z-30 w-72 bg-dark-900 border-r border-dark-700
        transform transition-transform duration-200 ease-in-out flex flex-col
        ${open ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `}>
        <div className="p-4 border-b border-dark-700 flex items-center justify-between">
          <h2 className="font-semibold text-dark-100">System Dashboard</h2>
          <button onClick={onClose} className="lg:hidden p-1 rounded hover:bg-dark-800">
            <svg className="w-5 h-5 text-dark-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-5">
          {/* Chat History */}
          <ChatHistory
            currentSessionId={currentSessionId}
            onSelectSession={onSelectSession}
            onNewChat={onNewChat}
            refreshTrigger={sessionRefresh}
          />

          <div className="border-t border-dark-700 pt-4">
            <h3 className="text-xs font-medium text-dark-400 uppercase tracking-wider mb-3">System</h3>
          </div>

          {/* Connection Status */}
          <section>
            <h3 className="text-xs font-medium text-dark-400 uppercase tracking-wider mb-2">Ollama Status</h3>
            <div className="bg-dark-800 rounded-lg p-3 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm text-dark-300">Connection</span>
                <div className="flex items-center gap-1.5">
                  <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
                  <span className={`text-xs ${isConnected ? 'text-green-400' : 'text-red-400'}`}>
                    {isConnected ? 'Online' : 'Offline'}
                  </span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-dark-300">LLM</span>
                <span className="text-xs text-dark-400">{health?.ollama?.llm_model || '—'}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-dark-300">LLM Ready</span>
                <span className={`text-xs ${health?.ollama?.llm_ready ? 'text-green-400' : 'text-yellow-400'}`}>
                  {health?.ollama?.llm_ready ? 'Yes' : 'No'}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-dark-300">Embeddings</span>
                <span className="text-xs text-dark-400">{health?.ollama?.embedding_model || '—'}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-dark-300">Embed Ready</span>
                <span className={`text-xs ${health?.ollama?.embedding_ready ? 'text-green-400' : 'text-yellow-400'}`}>
                  {health?.ollama?.embedding_ready ? 'Yes' : 'No'}
                </span>
              </div>
            </div>
          </section>

          {/* Documents */}
          <section>
            <h3 className="text-xs font-medium text-dark-400 uppercase tracking-wider mb-2">Knowledge Base</h3>
            <div className="bg-dark-800 rounded-lg p-3 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm text-dark-300">Chunks in DB</span>
                <span className="text-sm font-medium text-primary-400">
                  {docs?.ingested?.document_count ?? 0}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-dark-300">Available PDFs</span>
                <span className="text-sm font-medium text-dark-200">
                  {docs?.available_pdfs?.length ?? 0}
                </span>
              </div>
              {docs?.available_pdfs && docs.available_pdfs.length > 0 && (
                <div className="pt-1 space-y-1">
                  {docs.available_pdfs.map((pdf, idx) => (
                    <div key={idx} className="flex items-center gap-2 text-xs text-dark-400">
                      <svg className="w-3.5 h-3.5 text-red-400 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clipRule="evenodd" />
                      </svg>
                      <span className="truncate">{pdf}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </section>

          {/* Ingest Button */}
          <button
            onClick={handleIngest}
            disabled={ingesting}
            className="w-full py-2.5 px-4 rounded-lg bg-primary-600 hover:bg-primary-500 disabled:bg-primary-600/50 text-white text-sm font-medium transition-colors flex items-center justify-center gap-2"
          >
            {ingesting ? (
              <>
                <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
                Ingesting...
              </>
            ) : (
              <>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                </svg>
                Ingest PDFs
              </>
            )}
          </button>

          {ingestResult && (
            <p className={`text-xs text-center ${ingestResult.startsWith('Error') ? 'text-red-400' : 'text-green-400'}`}>
              {ingestResult}
            </p>
          )}

          {/* RAG Config */}
          <section>
            <h3 className="text-xs font-medium text-dark-400 uppercase tracking-wider mb-2">RAG Configuration</h3>
            <div className="bg-dark-800 rounded-lg p-3 space-y-2 text-sm">
              <div className="flex items-center justify-between">
                <span className="text-dark-300">Chunk Size</span>
                <span className="text-dark-400">{health?.config?.chunk_size ?? '—'}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-dark-300">Chunk Overlap</span>
                <span className="text-dark-400">{health?.config?.chunk_overlap ?? '—'}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-dark-300">Top K Results</span>
                <span className="text-dark-400">{health?.config?.top_k ?? '—'}</span>
              </div>
            </div>
          </section>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-dark-700">
          <p className="text-[10px] text-dark-600 text-center">
            MattressAI v1.0 — Custom RAG Pipeline
          </p>
        </div>
      </aside>
    </>
  );
}
