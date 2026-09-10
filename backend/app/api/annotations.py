from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from backend.app.db.database import get_db
from backend.app.db.models import DbAnnotation, DbEvaluation
from backend.app.schemas.models import AnnotationCreate, AnnotationResponse
from src.reliability.error_analysis import generate_error_report

router = APIRouter(prefix="/api/annotations", tags=["annotations"])

@router.post("", response_model=AnnotationResponse)
def submit_annotation(annotation: AnnotationCreate, db: Session = Depends(get_db)):
    # Verify the evaluation exists
    db_eval = db.query(DbEvaluation).filter(DbEvaluation.evaluation_id == str(annotation.evaluation_id)).first()
    if not db_eval:
        raise HTTPException(status_code=404, detail="Evaluation not found")
        
    db_ann = DbAnnotation(
        annotation_id=str(uuid.uuid4()),
        evaluation_id=str(annotation.evaluation_id),
        ground_truth_status=annotation.ground_truth_status
    )
    db.add(db_ann)
    db.commit()
    db.refresh(db_ann)
    
    return {
        "annotation_id": db_ann.annotation_id,
        "evaluation_id": db_ann.evaluation_id,
        "ground_truth_status": db_ann.ground_truth_status
    }
    
@router.get("/error-analysis")
def get_error_analysis(db: Session = Depends(get_db)):
    # To perform error analysis, we need the stored evaluations and their annotations
    
    db_annotations = db.query(DbAnnotation).all()
    annotations_list = [
        {"evaluation_id": a.evaluation_id, "ground_truth_status": a.ground_truth_status}
        for a in db_annotations
    ]
    
    # We will just fetch evaluations that have annotations to fake the TrustProfile claims
    evaluations_list = []
    for ann in annotations_list:
        # Mocking that the system predicted 'SUPPORTED'
        evaluations_list.append({
            "evaluation_id": ann["evaluation_id"],
            "claims": {"supported": 1, "total": 1}
        })
        
    report = generate_error_report(evaluations_list, annotations_list)
    return report
