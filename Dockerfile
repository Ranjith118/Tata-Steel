# ─────────────────────────────────────────────
#  Tata Steel Maintenance Wizard — HF Spaces
#  Single-container: FastAPI backend + React SPA
# ─────────────────────────────────────────────
FROM python:3.11-slim

# ── System deps ──────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ── HF Spaces requires a non-root user ───────
RUN useradd -m -u 1000 appuser

# ── Working directory ─────────────────────────
WORKDIR /app

# ── Copy requirements first (layer caching) ──
COPY backend/requirements.txt ./requirements.txt

# ── Install Python dependencies ───────────────
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir \
        chromadb>=0.4.22 \
        sentence-transformers>=2.3.0 \
        scikit-learn>=1.3.0 \
        xgboost>=2.0.0 \
        numpy>=1.24.0 \
        pandas>=2.0.0 \
        joblib>=1.3.0 \
        pypdf>=4.0.0 \
        groq>=0.9.0 \
        openai>=1.10.0 \
        langchain>=0.1.0 \
        langchain-community>=0.0.20 \
        langchain-core>=0.1.0 \
        tiktoken>=0.5.0 \
        python-dateutil>=2.8.0 \
        aiofiles>=0.8.0

# ── Copy backend ──────────────────────────────
COPY backend/ ./backend/

# ── Copy pre-built React SPA into static dir ─
COPY frontend/dist/ ./static/

# ── Create persistent data dirs ──────────────
RUN mkdir -p /app/data /app/chroma_db /app/models && \
    chown -R appuser:appuser /app

# ── Switch to non-root user ───────────────────
USER appuser

# ── Environment defaults (override via HF Secrets) ──
ENV DATABASE_URL=sqlite+aiosqlite:////app/data/maintenance_wizard.db
ENV CHROMA_DB_DIR=/app/chroma_db
ENV UPLOAD_DIR=/app/data
ENV LLM_PROVIDER=groq
ENV LLM_MODEL=llama-3.3-70b-versatile
ENV PORT=7860

# ── HF Spaces requires port 7860 ─────────────
EXPOSE 7860

# ── Start: run from backend dir so app.main resolves ──
WORKDIR /app/backend
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860", "--workers", "1"]
