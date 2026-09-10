from backend.app.schemas.models import Evidence

def detect_contradictions(claim_text: str, evidence: list[Evidence], mode: str = "fallback") -> float:
    """
    Returns a float representing 'possible_risk' of contradiction.
    """
    if mode == "fallback":
        # Heuristic: If we don't have enough evidence or if we just want a placeholder
        return 0.0
    else:
        # FUTURE ML MODE
        return 0.0
