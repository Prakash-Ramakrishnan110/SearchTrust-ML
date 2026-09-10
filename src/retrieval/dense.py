from backend.app.schemas.models import Source, Evidence
import uuid

class DenseRetriever:
    def __init__(self, sources: list[Source], ml_mode: bool = False):
        self.sources = sources
        self.ml_mode = ml_mode
        self.model = None
        
        if self.ml_mode:
            try:
                from sentence_transformers import SentenceTransformer
                # Defaulting to a small fast model
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
            except ImportError:
                print("Warning: sentence_transformers not installed. Falling back to heuristic.")
                self.ml_mode = False

    def search(self, query: str, top_k: int = 5) -> list[Evidence]:
        if not self.sources:
            return []
            
        if self.ml_mode and self.model:
            from sentence_transformers.util import cos_sim
            query_emb = self.model.encode(query)
            source_texts = [s.content for s in self.sources]
            doc_embs = self.model.encode(source_texts)
            
            scores = cos_sim(query_emb, doc_embs)[0].tolist()
            
            results = []
            for score, source in zip(scores, self.sources):
                results.append((score, source))
                
            results.sort(key=lambda x: x[0], reverse=True)
        else:
            # Fallback mock for dense retriever if ml_mode is false
            results = [(0.1, s) for s in self.sources]
            
        evidences = []
        for rank, (score, source) in enumerate(results[:top_k], start=1):
            evidences.append(Evidence(
                passage_id=uuid.uuid4(),
                source_id=source.source_id,
                rank=rank,
                retrieval_method="DENSE" if self.ml_mode else "DENSE_FALLBACK",
                retrieval_score=float(score)
            ))
            
        return evidences
