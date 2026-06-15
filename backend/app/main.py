"""Maintenance Wizard - FastAPI Backend Application."""
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base

# Import routers with fault tolerance — a single bad import won't crash the server
_routers = []
_failed_routers = []

def _safe_import(module_path, attr="router"):
    try:
        import importlib
        mod = importlib.import_module(module_path)
        _routers.append(getattr(mod, attr))
    except Exception as e:
        _failed_routers.append((module_path, str(e)))
        print(f"WARNING: Failed to import {module_path}: {e}")

_safe_import("app.routers.equipment")
_safe_import("app.routers.maintenance_logs")
_safe_import("app.routers.sensor_data")
_safe_import("app.routers.failure_reports")
_safe_import("app.routers.spare_parts")
_safe_import("app.routers.upload")
_safe_import("app.routers.dashboard")
_safe_import("app.routers.rag")
_safe_import("app.routers.anomaly")
_safe_import("app.routers.prediction")
_safe_import("app.routers.rca")
_safe_import("app.routers.recommendation")
_safe_import("app.routers.procurement")
_safe_import("app.routers.decision_support")
_safe_import("app.routers.learning")
_safe_import("app.routers.doc_intelligence")
_safe_import("app.routers.ai_actions")
_safe_import("app.routers.operational_data")
_safe_import("app.routers.search")
_safe_import("app.routers.intelligence_hub")
_safe_import("app.routers.fine_tuning")
_safe_import("app.routers.alerts")
_safe_import("app.routers.agent")


async def _background_startup():
    """Run heavy startup tasks in the background so the server starts fast."""
    # Warm up TF-IDF embedder with existing ChromaDB corpus
    try:
        from app.services.vector_db.chroma_service import get_vector_store
        from app.services.embeddings.embeddings import get_embedding_service
        vs  = get_vector_store()
        emb = get_embedding_service()
        texts = vs.get_all_texts(limit=500)
        if texts:
            emb.embed_texts(texts)
            print(f"Embedder warmed up with {len(texts)} corpus texts")
    except Exception as e:
        print(f"Embedder warm-up skipped: {e}")

    # Auto-train ML prediction models if not already trained
    try:
        from app.prediction.failure_model import get_failure_predictor, train_initial_failure_model
        from app.prediction.rul_model import get_rul_predictor, train_initial_rul_model
        fp = get_failure_predictor()
        rp = get_rul_predictor()
        if not fp.is_trained:
            await asyncio.to_thread(train_initial_failure_model)
            print("Failure prediction model trained on startup")
        if not rp.is_trained:
            await asyncio.to_thread(train_initial_rul_model)
            print("RUL prediction model trained on startup")
    except Exception as e:
        print(f"ML model auto-train skipped: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup and shutdown."""
    # Startup: Create database tables (fast — must complete before server accepts traffic)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Fire heavy tasks in the background — server is immediately ready to respond
    asyncio.create_task(_background_startup())

    yield

    # Shutdown: Close database connections
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version="9.0.0",
    description="Industrial Equipment Maintenance Management System for Steel Manufacturing Plants - Phase 9: Feedback Learning & Continuous Improvement",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(equipment.router)
app.include_router(maintenance_logs.router)
app.include_router(sensor_data.router)
app.include_router(failure_reports.router)
app.include_router(spare_parts.router)
app.include_router(upload.router)
app.include_router(dashboard.router)
app.include_router(rag.router)
app.include_router(anomaly.router)
app.include_router(prediction.router)
app.include_router(rca.router)
app.include_router(recommendation.router)
app.include_router(procurement.router)
app.include_router(decision_support.router)
app.include_router(learning.router)
app.include_router(doc_intelligence.router)
app.include_router(ai_actions.router)
app.include_router(operational_data.router)
app.include_router(search.router)
app.include_router(intelligence_hub.router)
app.include_router(fine_tuning.router)
app.include_router(alerts.router)
app.include_router(agent.router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": "9.0.0",
        "status": "running",
        "docs": "/docs",
    }