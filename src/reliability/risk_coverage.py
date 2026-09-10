def analyze_risk_coverage(claims: list) -> float:
    """
    Evaluates the density of SUPPORTED claims versus risky ones.
    Returns a score between 0 and 1, where 1 is total coverage.
    """
    if not claims:
        return 0.0
        
    supported = sum(1 for c in claims if c.status == "SUPPORTED")
    return supported / len(claims)
