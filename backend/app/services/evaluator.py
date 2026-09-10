import uuid
from backend.app.schemas.models import AnalyzeRequest, TrustProfile
from src.claims.extractor import extract_claims
from src.retrieval.hybrid import HybridRetriever
from src.verification.nli import verify_claim
from src.citations.mapper import map_citations
from src.temporal.analyzer import analyze_temporal_validity
from src.contradiction.detector import detect_contradictions
from src.source_quality.analyzer import analyze_source_quality
from src.provenance.graph import ProvenanceGraph
from src.reliability.calibration import calculate_calibration_metrics
from src.reliability.abstention import recommend_abstention

def run_evaluation(request: AnalyzeRequest, ml_mode: bool) -> TrustProfile:
    evaluation_id = uuid.uuid4()
    mode = "ml" if ml_mode else "fallback"
    
    graph = ProvenanceGraph()
    # Add QUERY node
    query_id = uuid.uuid4()
    graph.add_node(query_id, "QUERY", {"text": request.query})
    
    # Add ANSWER node
    answer_id = uuid.uuid4()
    graph.add_node(answer_id, "ANSWER", {"text": request.answer})
    graph.add_edge(query_id, answer_id, "generates")
    
    # 1. Extract Claims
    claims = extract_claims(request.answer, evaluation_id, mode)
    
    # 2. Retrieval Setup (Hybrid)
    retriever = HybridRetriever(request.sources, ml_mode=ml_mode)
    
    supported_count = 0
    refuted_count = 0
    unknown_count = 0
    needs_qual_count = 0
    
    # Track overall risks
    total_contradiction_risk = 0.0
    
    for claim in claims:
        claim_node_id = claim.claim_id
        graph.add_node(claim_node_id, "CLAIM", {"text": claim.text})
        graph.add_edge(answer_id, claim_node_id, "contains")
        
        # 3. Retrieve Evidence
        evidences = retriever.search(claim.text)
        evidence_texts = []
        for e in evidences:
            source_content = next((s.content for s in request.sources if s.source_id == e.source_id), "")
            evidence_texts.append(source_content)
            
            graph.add_node(e.passage_id, "EVIDENCE", {"text": source_content})
            graph.add_edge(claim_node_id, e.passage_id, "retrieved_for")
        
        # 4. Verification
        status = verify_claim(claim.text, evidence_texts, mode)
        claim.status = status
        
        # 5. Citation Mapping
        citation_info = map_citations(claim.text, request.citations, evidences)
        
        # 6. Contradiction Detection
        risk = detect_contradictions(claim.text, evidences, mode)
        total_contradiction_risk += risk
        
        if status == "SUPPORTED":
            supported_count += 1
        elif status == "REFUTED":
            refuted_count += 1
        elif status == "NEEDS_QUALIFICATION":
            needs_qual_count += 1
        else:
            unknown_count += 1
            
    # 7. Temporal Analysis
    freshness_warnings = analyze_temporal_validity(request.sources, request.query_time)
    
    # 8. Source Quality Analysis
    source_quality = analyze_source_quality(request.sources)
    
    # 9. Calibration
    # We will use mock predictions and truths for fallback mode.
    # In full ML mode, these would be collected from the NLI model's softmax outputs.
    predictions = [0.9] * len(claims) if claims else []
    truths = [1 if c.status == "SUPPORTED" else 0 for c in claims]
    calibration_metrics = calculate_calibration_metrics(predictions, truths, ml_mode)
    
    # 10. Abstention Logic
    overall_contradiction_risk = total_contradiction_risk / (len(claims) or 1)
    abstain = recommend_abstention(supported_count, len(claims), freshness_warnings, overall_contradiction_risk)
            
    return TrustProfile(
        evaluation_id=evaluation_id,
        claims={
            "total": len(claims),
            "supported": supported_count,
            "refuted": refuted_count,
            "unknown": unknown_count,
            "needs_qualification": needs_qual_count,
            "details": [{"text": c.text, "status": c.status} for c in claims]
        },
        citation={
            "coverage": 1.0 if request.citations else 0.0,
            "precision": 0.0,
            "entailment": 0.0
        },
        evidence={
            "recall_at_5": 0.0
        },
        temporal={
            "freshness_warnings": freshness_warnings
        },
        contradiction={
            "possible_risk": overall_contradiction_risk
        },
        calibration=calibration_metrics,
        abstention={
            "recommended": abstain
        }
    )
