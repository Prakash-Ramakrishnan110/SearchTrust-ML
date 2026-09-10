from backend.app.schemas.models import Source, Evidence
import uuid

class BM25Retriever:
    def __init__(self, sources: list[Source]):
        self.sources = sources

    def search(self, query: str, top_k: int = 5) -> list[Evidence]:
        # Heuristic fallback: simple word overlap
        results = []
        query_words = set(query.lower().split())
        
        for source in self.sources:
            content_words = set(source.content.lower().split())
            overlap = len(query_words.intersection(content_words))
            score = overlap / (len(query_words) + 1e-5)
            
            if score > 0:
                results.append((score, source))
                
        results.sort(key=lambda x: x[0], reverse=True)
        
        evidences = []
        for rank, (score, source) in enumerate(results[:top_k], start=1):
            evidences.append(Evidence(
                passage_id=uuid.uuid4(),
                source_id=source.source_id,
                rank=rank,
                retrieval_method="HEURISTIC_OVERLAP",
                retrieval_score=score
            ))
            
        return evidences
