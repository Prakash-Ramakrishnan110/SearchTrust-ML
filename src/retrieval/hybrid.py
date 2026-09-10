from backend.app.schemas.models import Source, Evidence
from src.retrieval.bm25 import BM25Retriever
from src.retrieval.dense import DenseRetriever

class HybridRetriever:
    def __init__(self, sources: list[Source], ml_mode: bool = False):
        self.bm25 = BM25Retriever(sources)
        self.dense = DenseRetriever(sources, ml_mode)

    def search(self, query: str, top_k: int = 5, k_rrf: int = 60) -> list[Evidence]:
        bm25_results = self.bm25.search(query, top_k=top_k)
        dense_results = self.dense.search(query, top_k=top_k)
        
        # RRF Fusion
        rrf_scores = {}
        source_map = {}
        
        for e in bm25_results:
            rrf_scores[e.source_id] = rrf_scores.get(e.source_id, 0.0) + (1.0 / (k_rrf + e.rank))
            source_map[e.source_id] = e
            
        for e in dense_results:
            rrf_scores[e.source_id] = rrf_scores.get(e.source_id, 0.0) + (1.0 / (k_rrf + e.rank))
            if e.source_id not in source_map:
                source_map[e.source_id] = e
                
        # Sort by RRF score
        fused = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        
        evidences = []
        for rank, (source_id, score) in enumerate(fused[:top_k], start=1):
            orig_evidence = source_map[source_id]
            # Create a new Evidence object for the hybrid result
            evidences.append(Evidence(
                passage_id=orig_evidence.passage_id,
                source_id=source_id,
                rank=rank,
                retrieval_method="HYBRID_RRF",
                retrieval_score=score
            ))
            
        return evidences
