from backend.app.schemas.models import Source

def analyze_source_quality(sources: list[Source]) -> dict:
    """
    Extracts transparent heuristic features for source quality.
    """
    features = {
        "publisher_known_ratio": 0.0,
        "primary_source_ratio": 0.0,
        "author_present_ratio": 0.0
    }
    
    if not sources:
        return features
        
    known_pubs = sum(1 for s in sources if s.publisher)
    authors = sum(1 for s in sources if s.author)
    primary = sum(1 for s in sources if s.source_type == "PRIMARY")
    
    total = len(sources)
    features["publisher_known_ratio"] = known_pubs / total
    features["author_present_ratio"] = authors / total
    features["primary_source_ratio"] = primary / total
    
    return features
