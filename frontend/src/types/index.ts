export interface Source {
  text: string;
  source: string;
  page: number;
  relevance_score: number;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: Source[];
  timestamp: Date;
  isStreaming?: boolean;
}

export interface HealthStatus {
  status: string;
  ollama: {
    status: string;
    url: string;
    llm_model: string;
    llm_ready: boolean;
    embedding_model: string;
    embedding_ready: boolean;
  };
  chromadb: {
    collection: string;
    document_count: number;
  };
  config: {
    chunk_size: number;
    chunk_overlap: number;
    top_k: number;
  };
}

export interface DocumentInfo {
  ingested: {
    collection: string;
    document_count: number;
  };
  available_pdfs: string[];
  pdf_directory: string;
}

export interface IngestResult {
  status: string;
  documents_processed: number;
  chunks_created: number;
  pdf_files: string[];
}

export interface ChatSession {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
  message_count: number;
}

export interface ChatSessionDetail {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
  messages: {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    sources: Source[];
    timestamp: string;
  }[];
}

export interface PipelineStep {
  step: string;
  label: string;
  icon: string;
  status: 'pending' | 'active' | 'done';
  duration_ms?: number;
  detail?: Record<string, any>;
}
