from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.config import settings
import uuid

settings.ml_mode = False

client = TestClient(app)

def test_annotation_flow():
    # 1. Create a fake evaluation
    eval_id = uuid.uuid4()
    
    # Normally we'd use the db session directly or create via API.
    # Since our mock uses DB, we need to ensure the DB has this evaluation.
    # But wait, we can just hit /api/analyze to create a real one.
    
    payload = {
        "query": "Is the sky blue?",
        "answer": "Yes, the sky is blue.",
        "query_time": "2023-01-01T00:00:00Z",
        "sources": [
            {
                "source_id": str(uuid.uuid4()),
                "title": "Science facts",
                "content": "The sky is blue.",
                "source_type": "PRIMARY"
            }
        ]
    }
    
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    evaluation_id = data["evaluation_id"]
    
    # 2. Submit annotation
    annotation_payload = {
        "evaluation_id": evaluation_id,
        "ground_truth_status": "SUPPORTED"
    }
    
    response = client.post("/api/annotations", json=annotation_payload)
    assert response.status_code == 200
    ann_data = response.json()
    assert ann_data["ground_truth_status"] == "SUPPORTED"
    
    # 3. Check error analysis report
    response = client.get("/api/annotations/error-analysis")
    assert response.status_code == 200
    report = response.json()
    assert report["total_analyzed"] >= 1
    assert "accuracy" in report
    
def test_abstention_logic():
    from src.reliability.abstention import recommend_abstention
    
    # Should abstain if no claims
    assert recommend_abstention(0, 0, 0, 0.0) == True
    
    # Should abstain if support ratio < 0.5
    assert recommend_abstention(1, 3, 0, 0.0) == True
    
    # Should not abstain if support ratio >= 0.5 and no warnings
    assert recommend_abstention(2, 3, 0, 0.0) == False
    
    # Should abstain if too many freshness warnings
    assert recommend_abstention(3, 3, 3, 0.0) == True
    
    # Should abstain if high contradiction risk
    assert recommend_abstention(3, 3, 0, 0.6) == True
