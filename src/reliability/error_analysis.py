def generate_error_report(evaluations: list[dict], annotations: list[dict]) -> dict:
    """
    Analyzes disagreements between system outputs and human annotations.
    """
    report = {
        "total_analyzed": 0,
        "false_positives": 0, # System said SUPPORTED, Human said REFUTED/UNKNOWN
        "false_negatives": 0, # System said REFUTED/UNKNOWN, Human said SUPPORTED
        "accuracy": 0.0
    }
    
    if not evaluations or not annotations:
        return report
        
    ann_map = {a["evaluation_id"]: a for a in annotations}
    
    correct = 0
    total = 0
    
    for eval_data in evaluations:
        e_id = eval_data["evaluation_id"]
        if e_id in ann_map:
            ann = ann_map[e_id]
            # simplified status determination based on TrustProfile claims summary
            sys_supported = eval_data.get("claims", {}).get("supported", 0)
            sys_total = eval_data.get("claims", {}).get("total", 1)
            
            sys_status = "SUPPORTED" if sys_supported / sys_total >= 0.5 else "UNSUPPORTED"
            hum_status = ann.get("ground_truth_status")
            
            total += 1
            if sys_status == hum_status:
                correct += 1
            else:
                if sys_status == "SUPPORTED" and hum_status != "SUPPORTED":
                    report["false_positives"] += 1
                elif sys_status != "SUPPORTED" and hum_status == "SUPPORTED":
                    report["false_negatives"] += 1
                    
    report["total_analyzed"] = total
    report["accuracy"] = correct / total if total > 0 else 0.0
    
    return report
