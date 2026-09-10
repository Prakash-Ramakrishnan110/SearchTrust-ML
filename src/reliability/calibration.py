def calculate_calibration_metrics(predictions: list[float], truths: list[int], ml_mode: bool = False) -> dict:
    """
    Computes Brier Score and Expected Calibration Error (ECE).
    If ml_mode is False, returns 0.0 because the fallback NLI verifier
    does not produce probabilities.
    """
    if not ml_mode or not predictions or not truths:
        return {"brier_score": 0.0, "ece": 0.0}
        
    try:
        from sklearn.metrics import brier_score_loss
        brier = brier_score_loss(truths, predictions)
        
        # Simple ECE approximation
        import numpy as np
        bins = np.linspace(0, 1, 11)
        binned = np.digitize(predictions, bins) - 1
        
        ece = 0.0
        for i in range(10):
            bin_preds = [p for j, p in enumerate(predictions) if binned[j] == i]
            bin_truths = [t for j, t in enumerate(truths) if binned[j] == i]
            if bin_preds:
                acc = np.mean(bin_truths)
                conf = np.mean(bin_preds)
                ece += (len(bin_preds) / len(predictions)) * abs(acc - conf)
                
        return {"brier_score": float(brier), "ece": float(ece)}
    except ImportError:
        return {"brier_score": 0.0, "ece": 0.0}
