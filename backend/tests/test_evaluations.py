from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.config import settings
import uuid
from datetime import datetime, timezone, timedelta

# Force fallback mode for deterministic testing
settings.ml_mode = False

client = TestClient(app)

def test_analyze_endpoint():
    four_years_ago = (datetime.now(timezone.utc) - timedelta(days=4*365)).isoformat()
    
    payload = {
        "query": "Who is the current CEO of Example Company?",
        "answer": "Alex Smith became CEO in 2019. He remains the current CEO.",
        "query_time": datetime.now(timezone.utc).isoformat(),
        "citations": [{"id": "c1", "text": "citation 1"}],
        "sources": [
            {
                "source_id": str(uuid.uuid4()),
                "title": "Company announcement",
                "content": "Alex Smith became CEO of Example Company in 2019.",
                "source_type": "NEWS",
                "published_at": four_years_ago
            }
        ]
    }
    
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    # Verify Trust Profile structure
    assert "evaluation_id" in data
    assert "claims" in data
    assert "temporal" in data
    
    assert data["claims"]["total"] > 0
    
    # The source is 4 years old, which should trigger a freshness warning
    assert data["temporal"]["freshness_warnings"] == 1
