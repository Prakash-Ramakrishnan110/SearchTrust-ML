from datetime import datetime, timezone
from backend.app.schemas.models import Source

def analyze_temporal_validity(sources: list[Source], query_time: datetime | None = None) -> int:
    """
    Returns the number of freshness warnings (POTENTIALLY_OUTDATED or OUTDATED).
    """
    if query_time is None:
        query_time = datetime.now(timezone.utc)
        
    warnings = 0
    
    for source in sources:
        # Determine the effective date of the source
        source_date = source.event_date or source.updated_at or source.published_at or source.retrieved_at
        if source_date:
            try:
                # Basic heuristic for MVP: if source is > 3 years older than query
                if (query_time.year - source_date.year) > 3:
                    warnings += 1
            except AttributeError:
                pass
                
    return warnings
