<div align="center">

# 🛏️ MattressAI

### Professional RAG System for Mattress Knowledge

**Custom Retrieval-Augmented Generation pipeline powered by local LLM**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)](https://react.dev)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-000000?logo=ollama)](https://ollama.com)
[![FAISS](https://img.shields.io/badge/FAISS-Vector%20Store-FF6B6B)](https://github.com/facebookresearch/faiss)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6-3178C6?logo=typescript&logoColor=white)](https://typescriptlang.org)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-3.4-06B6D4?logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://docker.com)

---

*A production-ready RAG solution that ingests PDF documents, creates vector embeddings, and uses a local DeepSeek LLM via Ollama to answer questions with source citations. Built with a custom pipeline — no LangChain dependency.*

[Features](#-features) · [Architecture](#-architecture) · [Quick Start](#-quick-start) · [API Docs](#-api-documentation) · [Configuration](#-configuration)

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔒 **Fully Local** | All data stays on your machine — no external API calls, complete data privacy |
| 📄 **PDF Ingestion** | Automatic text extraction, chunking, and embedding of PDF documents |
| 🧠 **Custom RAG Pipeline** | Hand-crafted Retrieve → Prompt → Generate pipeline — no framework bloat |
| ⚡ **Streaming Responses** | Real-time token streaming via Server-Sent Events (SSE) |
| 📚 **Source Citations** | Every answer includes clickable source references (PDF name, page, relevance %) |
| 🎨 **Professional UI** | React + TailwindCSS chat interface with dark theme |
| 📊 **System Dashboard** | Real-time monitoring of Ollama status, FAISS stats, and RAG config |
| 🐳 **Docker Ready** | One-command deployment with Docker Compose |
| 📤 **File Upload** | Upload new PDFs via API or UI |
| 🔄 **Chat History** | Context-aware follow-up questions using conversation history |

---

## 🏗 Architecture

```
┌──────────────────────┐    HTTP/REST + SSE    ┌───────────────────────────────┐
│                      │ ◄───────────────────► │                               │
│    React Frontend    │                       │      FastAPI Backend           │
│                      │                       │                               │
│  • Chat Interface    │                       │  POST /api/chat    → Query    │
│  • Source Citations   │                       │  GET  /api/documents → List   │
│  • System Dashboard  │                       │  POST /api/ingest  → Ingest   │
│  • Streaming Display │                       │  POST /api/upload  → Upload   │
│                      │                       │  GET  /api/health  → Status   │
│  Port: 5173 (dev)    │                       │  Port: 8000                    │
│  Port: 3000 (docker) │                       │                               │
└──────────────────────┘                       └──────────────┬────────────────┘
                                                              │
                                           ┌──────────────────┼──────────────────┐
                                           │                  │                  │
                                           ▼                  ▼                  ▼
                                  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
                                  │    FAISS     │  │  Ollama API  │  │    PDF       │
                                  │              │  │              │  │  Ingestion   │
                                  │  • Cosine    │  │  • DeepSeek  │  │              │
                                  │    Similarity│  │    r1:1.5b   │  │  • PyPDF2    │
                                  │  • Persistent│  │  • nomic-    │  │  • Recursive │
                                  │    Storage   │  │    embed-text│  │    Chunking  │
                                  └──────────────┘  └──────────────┘  └──────────────┘
```

### RAG Pipeline Flow

```
User Question
      │
      ▼
┌─────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Embed     │───►│   Retrieve   │───►│   Build      │───►│   Generate   │
│   Query     │    │   Top-K      │    │   Prompt     │    │   Answer     │
│             │    │   Chunks     │    │   + Context  │    │   (Stream)   │
│ nomic-embed │    │  FAISS       │    │  System +    │    │  DeepSeek    │
│   -text     │    │  Cosine Sim  │    │  Sources     │    │   r1:1.5b   │
└─────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
                                                                  │
                                                                  ▼
                                                          ┌──────────────┐
                                                          │   Response   │
                                                          │   + Source   │
                                                          │   Citations  │
                                                          └──────────────┘
```

### Document Ingestion Flow

```
PDF Files ──► Text Extraction ──► Recursive Chunking ──► Embedding ──► FAISS Index
              (PyPDF2)            (500 chars, 50          (nomic-       (Cosine
                                   char overlap)           embed-text)   similarity)
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **Ollama** installed and running ([Install Guide](https://ollama.com/download))

### Step 1: Pull Required Models

```bash
ollama pull deepseek-r1:1.5b
ollama pull nomic-embed-text
```

### Step 2: Clone & Setup Backend

```bash
cd rag

# Create Python virtual environment
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt
pip install reportlab   # For generating sample PDFs
```

### Step 3: Generate Sample PDFs & Ingest

```bash
# Generate demo mattress knowledge PDFs
python generate_sample_pdfs.py

# Ingest PDFs into vector store
python ingest.py
```

### Step 4: Start Backend

```bash
uvicorn app.main:app --reload --port 8000
```

### Step 5: Setup & Start Frontend

```bash
# In a new terminal
cd frontend
npm install
npm run dev
```

### Step 6: Open the App

Navigate to **http://localhost:5173** and start asking about mattresses!

---

### 🐳 Docker Deployment

```bash
# From the project root
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

> **Note:** Ollama must be running on the host machine. Docker services connect via `host.docker.internal`.

---

## 📡 API Documentation

### `GET /api/health`

Health check — returns Ollama connectivity, model status, and vector store statistics.

```json
{
  "status": "healthy",
  "ollama": {
    "status": "connected",
    "llm_model": "deepseek-r1:1.5b",
    "llm_ready": true,
    "embedding_model": "nomic-embed-text",
    "embedding_ready": true
  },
  "chromadb": {
    "collection": "mattress_docs",
    "document_count": 87
  },
  "config": {
    "chunk_size": 500,
    "chunk_overlap": 50,
    "top_k": 5
  }
}
```

### `POST /api/chat`

Send a question and receive a streaming (SSE) or full response with source citations.

**Request:**
```json
{
  "query": "What type of mattress is best for back pain?",
  "chat_history": [],
  "stream": true
}
```

**SSE Response Events:**
```
data: {"type": "sources", "data": [{"text": "...", "source": "buying_guide.pdf", "page": 5, "relevance_score": 0.93}]}
data: {"type": "token", "data": "Based"}
data: {"type": "token", "data": " on"}
data: {"type": "token", "data": " the"}
...
data: {"type": "done"}
```

### `POST /api/ingest`

Ingest all PDFs from the `backend/data/pdfs/` directory.

```json
{
  "status": "success",
  "documents_processed": 2,
  "chunks_created": 87,
  "pdf_files": ["mattress_buying_guide.pdf", "mattress_care_maintenance_guide.pdf"]
}
```

### `POST /api/upload`

Upload a new PDF file for ingestion (multipart form-data).

### `GET /api/documents`

List available and ingested documents with statistics.

---

## ⚙️ Configuration

All settings can be configured via environment variables or `.env` file:

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama API endpoint |
| `LLM_MODEL` | `deepseek-r1:1.5b` | Generation model name |
| `EMBEDDING_MODEL` | `nomic-embed-text` | Embedding model name |
| `CHUNK_SIZE` | `500` | Maximum characters per chunk |
| `CHUNK_OVERLAP` | `50` | Character overlap between chunks |
| `TOP_K` | `5` | Number of chunks retrieved per query |
| `CHROMA_PERSIST_DIR` | `./vector_data` | FAISS index storage directory |
| `FRONTEND_URL` | `http://localhost:5173` | Allowed CORS origin |

---

## 🗂 Project Structure

```
rag/
├── backend/
│   ├── app/
│   │   ├── main.py                # FastAPI application entry point
│   │   ├── config.py              # Pydantic Settings configuration
│   │   ├── rag_pipeline.py        # RAG orchestrator (retrieve → prompt → generate)
│   │   ├── api/
│   │   │   ├── chat.py            # POST /api/chat endpoint (SSE streaming)
│   │   │   ├── documents.py       # Document management + ingestion endpoints
│   │   │   └── health.py          # System health check endpoint
│   │   └── core/
│   │       ├── pdf_loader.py      # PDF text extraction (PyPDF2)
│   │       ├── chunker.py         # Recursive text splitter with overlap
│   │       ├── embeddings.py      # Ollama embedding API wrapper
│   │       ├── vector_store.py    # FAISS index operations (add, query, stats)
│   │       ├── retriever.py       # Similarity search + scoring
│   │       ├── prompt.py          # RAG prompt template with citation format
│   │       └── generator.py       # Ollama chat API wrapper (streaming)
│   ├── data/pdfs/                 # PDF document storage
│   ├── ingest.py                  # Standalone ingestion script
│   ├── generate_sample_pdfs.py    # Demo PDF generator
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests/
│       ├── test_chunker.py        # Chunking unit tests
│       └── test_prompt.py         # Prompt building unit tests
├── frontend/
│   ├── src/
│   │   ├── App.tsx                # Root component with layout
│   │   ├── components/
│   │   │   ├── ChatWindow.tsx     # Chat area with input + suggested questions
│   │   │   ├── MessageBubble.tsx  # Message display with markdown + sources
│   │   │   ├── SourceCard.tsx     # Expandable source citation card
│   │   │   ├── Sidebar.tsx        # System dashboard (status + docs + config)
│   │   │   └── Header.tsx         # App header with connection status
│   │   ├── hooks/useChat.ts       # Chat state + streaming logic
│   │   ├── services/api.ts        # Backend API client
│   │   └── types/index.ts         # TypeScript type definitions
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── Dockerfile
│   └── nginx.conf                 # Production reverse proxy config
├── docker-compose.yml             # Multi-container orchestration
├── .env.example                   # Environment variable template
├── .gitignore
└── README.md
```

---

## 🧪 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **LLM** | DeepSeek R1 1.5B (via Ollama) | Text generation |
| **Embeddings** | nomic-embed-text (via Ollama) | Document & query embedding |
| **Vector Store** | FAISS (persistent) | Similarity search |
| **Backend** | FastAPI + Uvicorn | REST API + SSE streaming |
| **Frontend** | React 18 + TypeScript | Chat UI |
| **Styling** | TailwindCSS | Professional design system |
| **PDF Processing** | PyPDF2 | Text extraction |
| **HTTP Client** | httpx (async) | Ollama API communication |
| **Containerization** | Docker + Docker Compose | Deployment |

---

## 🔧 How It Works

### 1. Document Ingestion
PDFs are loaded with **PyPDF2**, extracting text page by page. The text is then split into overlapping chunks using a **recursive character splitter** that tries to split on paragraph breaks (`\n\n`), line breaks (`\n`), sentence endings (`. `), and finally spaces — preserving semantic coherence. Each chunk is embedded using **nomic-embed-text** (768-dimensional vectors) via the Ollama API and stored in a **FAISS** index with metadata (source file, page number, chunk index). The index is persisted to disk for durability.

### 2. Retrieval
When a user asks a question, the query is embedded using the same model. **FAISS** performs a cosine similarity search (inner product on L2-normalized vectors) to find the top-K most relevant chunks. Each result includes a relevance score converted from cosine distance.

### 3. Prompt Construction
Retrieved chunks are formatted into a context block with source attribution. A carefully crafted system prompt instructs the LLM to:
- Answer only from provided context
- Cite sources with `[Source: filename, Page X]` format
- Acknowledge when information is insufficient

### 4. Generation
The constructed prompt is sent to **DeepSeek R1 1.5B** via Ollama's chat API. Responses stream token-by-token via SSE to the frontend, providing a smooth typing effect.

### 5. Citation Display
Sources are sent as the first SSE event, allowing the frontend to prepare citation cards. Each source shows the PDF name, page number, relevance percentage, and an expandable text preview.

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Ollama not connecting | Ensure Ollama is running: `ollama serve` |
| Model not found | Pull models: `ollama pull deepseek-r1:1.5b` and `ollama pull nomic-embed-text` |
| No chunks after ingestion | Check that PDFs have extractable text (not scanned images) |
| CORS errors | Verify `FRONTEND_URL` in `.env` matches your frontend origin |
| Docker can't reach Ollama | Use `host.docker.internal:11434` or `network_mode: host` |
| Slow responses | DeepSeek 1.5B is lightweight; for faster responses, ensure sufficient RAM |
| Import error for faiss | Install with `pip install faiss-cpu` |

---

## 📈 Scaling for Production

This solution is designed as a demo/POC. For production scaling, consider:

- **Larger LLM**: Upgrade to DeepSeek 7B/14B or Llama 3 for better response quality
- **GPU Acceleration**: Run Ollama with GPU support for faster inference
- **Production Vector DB**: Migrate from FAISS to Qdrant, Pinecone, or Weaviate for distributed search
- **Authentication**: Add JWT/OAuth2 authentication to the API
- **Rate Limiting**: Add request throttling for public deployments
- **Monitoring**: Integrate with Prometheus/Grafana for observability
- **Caching**: Add Redis caching for frequent queries

---

<div align="center">

**Built with ❤️ as a professional RAG showcase**

*Custom Pipeline • Local LLM • Full Privacy • Source Citations*

</div>
#   M a t t r e s s A I  
 