import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Float
from backend.app.db.database import Base

class DbEvaluation(Base):
    __tablename__ = "evaluations"
    evaluation_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    query = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    profile_data = Column(String)  # JSON string of the TrustProfile
    created_at = Column(DateTime, default=datetime.utcnow)

class DbClaim(Base):
    __tablename__ = "claims"
    claim_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    evaluation_id = Column(String, index=True)
    text = Column(String, nullable=False)
    claim_type = Column(String, default="FACTUAL")
    status = Column(String, default="UNKNOWN")

class DbSource(Base):
    __tablename__ = "sources"
    source_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String)
    content = Column(String)
    source_type = Column(String, default="UNKNOWN")

class DbEvidence(Base):
    __tablename__ = "evidence"
    passage_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source_id = Column(String, index=True)
    retrieval_method = Column(String)
    retrieval_score = Column(Float)

class DbAnnotation(Base):
    __tablename__ = "annotations"
    annotation_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    evaluation_id = Column(String, index=True)
    ground_truth_status = Column(String, nullable=False)
