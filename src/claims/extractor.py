import uuid
import os
from backend.app.schemas.models import Claim

def extract_claims(answer: str, evaluation_id: uuid.UUID, mode: str = "fallback") -> list[Claim]:
    claims = []
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if mode == "ml" and api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            prompt = f"Extract the specific factual claims from the following text. Return ONLY a bulleted list of claims, one per line. Text: '{answer}'"
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt
            )
            
            lines = [line.strip().strip('-* ') for line in response.text.split('\n') if len(line.strip()) > 5]
            for s in lines:
                claims.append(
                    Claim(
                        claim_id=uuid.uuid4(),
                        evaluation_id=evaluation_id,
                        text=s,
                        claim_type="FACTUAL",
                        status="UNKNOWN"
                    )
                )
            return claims
        except Exception as e:
            print(f"Gemini API error during extraction: {e}")
            # Fall through to fallback
            
    # Fallback Deterministic heuristic: split by period
    sentences = [s.strip() for s in answer.split('.') if len(s.strip()) > 10]
    for s in sentences:
        claims.append(
            Claim(
                claim_id=uuid.uuid4(),
                evaluation_id=evaluation_id,
                text=s + ".",
                claim_type="FACTUAL",
                status="UNKNOWN"
            )
        )
    return claims
