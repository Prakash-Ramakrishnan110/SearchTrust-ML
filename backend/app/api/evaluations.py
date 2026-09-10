import json
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from backend.app.schemas.models import AnalyzeRequest, TrustProfile
from backend.app.services.evaluator import run_evaluation
from backend.app.config import settings
from backend.app.db.database import get_db
from backend.app.db.models import DbEvaluation

router = APIRouter()

@router.post("/analyze", response_model=TrustProfile)
def analyze(request: AnalyzeRequest, db: Session = Depends(get_db)):
    profile = run_evaluation(request, settings.ml_mode)
    
    # Save the evaluation to DB so we can annotate it later
    db_eval = DbEvaluation(
        evaluation_id=str(profile.evaluation_id),
        query=request.query,
        answer=request.answer,
        profile_data=profile.model_dump_json() if hasattr(profile, 'model_dump_json') else profile.json()
    )
    db.add(db_eval)
    db.commit()
    
    return profile

@router.get("/evaluations")
def list_evaluations(db: Session = Depends(get_db), limit: int = 50):
    evals = db.query(DbEvaluation).order_by(desc(DbEvaluation.created_at)).limit(limit).all()
    
    results = []
    for e in evals:
        # Some old records might not have profile_data
        parsed_profile = None
        if e.profile_data:
            try:
                parsed_profile = json.loads(e.profile_data)
            except:
                pass
                
        results.append({
            "evaluation_id": e.evaluation_id,
            "query": e.query,
            "answer": e.answer,
            "created_at": e.created_at.isoformat() if e.created_at else None,
            "trust_profile": parsed_profile
        })
        
    return results

@router.get("/search")
def web_search(q: str):
    try:
        from ddgs import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(q, max_results=3))
            
        formatted_sources = []
        for r in results:
            formatted_sources.append({
                "source_id": str(uuid.uuid4()),
                "title": r.get("title", "Web Result"),
                "content": r.get("body", ""),
                "source_type": "NEWS"
            })
        return formatted_sources
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"Web search failed: {str(e)}")
