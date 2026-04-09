@echo off
title MattressAI Launcher
echo ============================================
echo         MattressAI - Starting Up
echo ============================================
echo.

:: Check Ollama is running
echo [1/6] Checking Ollama...
ollama list >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Ollama is not running. Please start Ollama first.
    echo Download from https://ollama.com/download
    pause
    exit /b 1
)
echo       Ollama is running.

:: Pull models if not already available
echo [2/6] Ensuring models are available...
ollama list | findstr /i "deepseek-r1:1.5b" >nul 2>&1
if %errorlevel% neq 0 (
    echo       Pulling deepseek-r1:1.5b ...
    ollama pull deepseek-r1:1.5b
)
ollama list | findstr /i "nomic-embed-text" >nul 2>&1
if %errorlevel% neq 0 (
    echo       Pulling nomic-embed-text ...
    ollama pull nomic-embed-text
)
echo       Models ready.

:: Setup backend venv if needed
echo [3/6] Setting up backend...
cd /d "%~dp0backend"
if not exist "venv" (
    echo       Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate.bat

:: Install dependencies
echo [4/6] Installing backend dependencies...
pip install -r requirements.txt -q

:: Generate sample PDFs and ingest if no vector store exists
if not exist "chroma_data\index.faiss" (
    echo [5/6] Ingesting documents into vector store...
    if not exist "data\pdfs\mattress_buying_guide.pdf" (
        python generate_sample_pdfs.py
    )
    python ingest.py
) else (
    echo [5/6] Vector store already exists, skipping ingestion.
)

:: Start backend in background
echo [6/6] Launching backend and frontend...
echo.
echo       Starting backend on http://localhost:8000
start "MattressAI Backend" cmd /k "cd /d "%~dp0backend" && call venv\Scripts\activate.bat && uvicorn app.main:app --reload --port 8000"

:: Setup and start frontend
cd /d "%~dp0frontend"
if not exist "node_modules" (
    echo       Installing frontend dependencies...
    call npm install
)
echo       Starting frontend on http://localhost:5173
start "MattressAI Frontend" cmd /k "cd /d "%~dp0frontend" && npm run dev"

:: Wait a moment then open browser
timeout /t 5 /nobreak >nul
start http://localhost:5173

echo.
echo ============================================
echo   MattressAI is running!
echo   Frontend: http://localhost:5173
echo   Backend:  http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo ============================================
echo.
echo Close the Backend and Frontend terminal windows to stop.
pause
