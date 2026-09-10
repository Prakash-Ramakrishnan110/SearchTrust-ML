import os

def verify_claim(claim: str, evidence_texts: list[str], mode: str = "fallback") -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if mode == "ml" and api_key and evidence_texts:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            
            combined_evidence = "\n".join(evidence_texts)
            prompt = f"""
            You are a strict fact-checker. Determine if the following CLAIM is strictly SUPPORTED, REFUTED, or UNKNOWN based ONLY on the provided EVIDENCE.
            Do not use outside knowledge. Answer with exactly one word: SUPPORTED, REFUTED, or UNKNOWN.
            
            CLAIM: {claim}
            
            EVIDENCE:
            {combined_evidence}
            """
            
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt
            )
            result = response.text.strip().upper()
            
            if "SUPPORTED" in result: return "SUPPORTED"
            if "REFUTED" in result: return "REFUTED"
            return "UNKNOWN"
        except Exception as e:
            print(f"Gemini API error during verification: {e}")
            # Fall through to fallback
            
    # Fallback Heuristic verification: check if majority of claim words are in evidence
    claim_words = set(claim.lower().strip('.').split())
    for text in evidence_texts:
        text_words = set(text.lower().split())
        overlap = len(claim_words.intersection(text_words))
        if len(claim_words) > 0 and overlap / len(claim_words) > 0.6:
            return "SUPPORTED"
    return "UNKNOWN"
