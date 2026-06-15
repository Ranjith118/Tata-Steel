FROM python:3.11-slim

# System deps
RUN apt-get update && apt-get install -y \
    gcc g++ cmake libffi-dev libssl-dev curl \
    && rm -rf /var/lib/apt/lists/*

# HF Spaces requires non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Install deps
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt --no-cache-dir

# Copy backend code
COPY backend/ ./backend/

# Create data dirs with correct permissions
RUN mkdir -p /app/backend/data /app/backend/chroma_db && \
    chown -R appuser:appuser /app

USER appuser

# HF Spaces MUST use port 7860
EXPOSE 7860

CMD ["sh", "-c", "cd /app/backend && uvicorn app.main:app --host 0.0.0.0 --port 7860 --workers 1"]
