---
title: Tata Steel Project
emoji: 🏭
colorFrom: blue
colorTo: gray
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# Maintenance Wizard — Tata Steel

AI-powered Industrial Equipment Maintenance Management System for steel manufacturing plants.

## Features

- **Predictive Maintenance** — ML models predict failure probability and Remaining Useful Life (RUL)
- **Anomaly Detection** — Isolation Forest flags abnormal sensor readings
- **Root Cause Analysis** — LLM-powered RCA reports with confidence scoring
- **RAG Chat Assistant** — Groq LLaMA 3.3 70B answers questions grounded in maintenance manuals
- **Document Intelligence** — PDF ingestion, chunking, and AI analysis
- **Alert Engine** — Health score thresholds triggering real-time alerts
- **Decision Support** — Plant-level criticality, risk scoring, bottleneck detection
- **Feedback Learning** — Continuous improvement loop with technician feedback

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + Uvicorn |
| Database | SQLite (auto-created) |
| Vector DB | ChromaDB |
| LLM | Groq API (LLaMA 3.3 70B) |
| Embeddings | Sentence Transformers |
| ML | scikit-learn + XGBoost |
| Frontend | React 18 + Vite + Tailwind CSS |

## Environment Variables (set in HF Space Secrets)

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key (required for AI features) |
| `LLM_PROVIDER` | `groq` (default) |
| `LLM_MODEL` | `llama-3.3-70b-versatile` (default) |
