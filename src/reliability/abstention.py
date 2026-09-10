def recommend_abstention(supported_claims: int, total_claims: int, freshness_warnings: int, contradiction_risk: float) -> bool:
    """
    Heuristic logic to recommend abstention from generating an answer.
    """
    if total_claims == 0:
        return True # Abstain if no claims can be extracted
        
    support_ratio = supported_claims / total_claims
    
    if support_ratio < 0.5:
        return True # More than half the claims are unsupported or refuted
        
    if freshness_warnings > 2:
        return True # Too much outdated evidence
        
    if contradiction_risk > 0.5:
        return True # High contradiction risk among sources
        
    return False
