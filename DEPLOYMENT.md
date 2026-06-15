# Deploying to Hugging Face Spaces

## Architecture

Single Docker container on HF Spaces:
- FastAPI backend (Uvicorn, port 7860)
- React SPA served as static files from FastAPI itself
- SQLite database (persisted in /app/data)
- ChromaDB vector store (persisted in /app/chroma_db)

---

## Step 1 — Build the React frontend

Run this once locally before pushing (the dist/ folder goes into the repo):

```bash
cd frontend
npm install
npm run build
```

The `frontend/dist/` folder will be committed to git and copied into the Docker image.

---

## Step 2 — Create a Hugging Face Space

1. Go to https://huggingface.co/spaces
2. Click **"Create new Space"**
3. Fill in:
   - **Space name:** `tata-steel-maintenance` (or any name you like)
   - **License:** MIT
   - **SDK:** **Docker**  ← important
   - **Visibility:** Public or Private
4. Click **"Create Space"**

---

## Step 3 — Push code to the Space

HF Spaces is a Git repository. Clone it and push your code:

```bash
# Install Git LFS first (for large model files if any)
git lfs install

# Clone your new Space (replace YOUR_USERNAME and SPACE_NAME)
git clone https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME

# Copy project files into the cloned folder
# (or add the HF remote to your existing repo)
cd "Tata steel Maintenance"
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME

# Push to HF
git add .
git commit -m "Initial deployment"
git push hf main
```

> ⚠️  Make sure `backend/.env` is in `.gitignore` and NOT pushed!

---

## Step 4 — Set Secret Environment Variables

In your Space settings on HF:

1. Go to **Settings → Variables and secrets**
2. Add the following **Secrets** (not Variables — secrets are encrypted):

| Secret name | Value |
|---|---|
| `GROQ_API_KEY` | Your Groq API key from https://console.groq.com |

Optional overrides (can be Variables):

| Variable name | Default value |
|---|---|
| `LLM_PROVIDER` | `groq` |
| `LLM_MODEL` | `llama-3.3-70b-versatile` |

---

## Step 5 — Wait for the build

HF Spaces will:
1. Detect the `Dockerfile` at the repo root
2. Build the Docker image (~5–10 min first time due to ML deps)
3. Start the container on port 7860
4. Make the app available at: `https://YOUR_USERNAME-SPACE_NAME.hf.space`

You can watch build logs in the **Logs** tab of your Space.

---

## What the app exposes

| URL | Description |
|---|---|
| `https://…hf.space/` | React frontend (LandingPage) |
| `https://…hf.space/dashboard` | Main dashboard |
| `https://…hf.space/api-docs` | FastAPI Swagger UI |
| `https://…hf.space/health` | Health check JSON |
| `https://…hf.space/api/info` | App info JSON |

---

## Troubleshooting

**Build fails with OOM / timeout**
- The ML deps (sentence-transformers, chromadb, scikit-learn) are heavy.
- HF free tier gives 16 GB RAM. If it fails, upgrade to a paid Space or remove unused deps.

**App starts but AI features don't work**
- Check that `GROQ_API_KEY` secret is set correctly in Space settings.
- Check the Logs tab for `GROQ_API_KEY not found` errors.

**React pages show blank / 404**
- The SPA catch-all in `main.py` handles all non-API routes.
- If you see a raw JSON response on `/{route}`, the static dir wasn't copied — ensure `frontend/dist/` is committed.

**ChromaDB / embeddings reset on restart**
- HF free Spaces don't have persistent storage. Data resets on every restart.
- For persistence, use a [HF Space with a persistent dataset](https://huggingface.co/docs/hub/spaces-storage) or upgrade to a paid tier.

---

## Local development (unchanged)

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

Frontend dev server at http://localhost:5173, API at http://localhost:8000.
