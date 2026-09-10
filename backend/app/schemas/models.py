import uuid
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID

class Source(BaseModel):
    source_id: UUID
    title: str
    url: Optional[str] = None
    publisher: Optional[str] = None
    author: Optional[str] = None
    source_type: str = "UNKNOWN"
    published_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    event_date: Optional[datetime] = None
    retrieved_at: Optional[datetime] = None
    content: str

class Claim(BaseModel):
    claim_id: UUID
    evaluation_id: UUID
    text: str
    sentence_id: Optional[str] = None
    claim_type: str = "FACTUAL"
    materiality: str = "MEDIUM"
    temporal_dependency: bool = False
    citation_ids: List[str] = []
    status: str = "UNKNOWN"

class Evidence(BaseModel):
    passage_id: UUID
    source_id: UUID
    rank: int
    retrieval_method: str
    retrieval_score: float

class TrustProfile(BaseModel):
    evaluation_id: UUID
    claims: dict  # Includes total, supported, refuted, unknown, needs_qualification, details
    citation: dict
    evidence: dict
    temporal: dict
    contradiction: dict
    calibration: dict
    abstention: dict

class AnalyzeRequest(BaseModel):
    query: str
    answer: str
    query_time: Optional[datetime] = None
    citations: List[dict] = []
    sources: List[Source] = []

class AnnotationCreate(BaseModel):
    evaluation_id: uuid.UUID
    ground_truth_status: str

class AnnotationResponse(AnnotationCreate):
    annotation_id: uuid.UUID
