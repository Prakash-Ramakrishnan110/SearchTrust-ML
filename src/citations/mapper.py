def map_citations(claim_text: str, citations: list, evidence: list) -> dict:
    # Heuristic: just check if there are citations
    return {
        "citation_present": len(citations) > 0,
        "citation_entails_claim": 0.0,
    }
