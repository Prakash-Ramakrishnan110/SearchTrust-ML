from fastapi import FastAPI
from backend.app.config import settings
from backend.app.db.database import engine, Base
from backend.app.db import models
from backend.app.api.evaluations import router as eval_router
from backend.app.api.annotations import router as annot_router

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SearchTrust ML",
    description="An open, calibrated evaluation protocol for claim-level grounding and citation correctness in AI search answers.",
    version=settings.api_version,
)

app.include_router(eval_router, prefix="/api")
app.include_router(annot_router)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "version": settings.api_version, "environment": settings.env}
