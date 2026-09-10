import json
import argparse
import requests
from pathlib import Path
import time

def run_experiment(input_path, api_url, output_path):
    print(f"Loading adapted dataset from {input_path}...")
    with open(input_path, "r", encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]

    print(f"Loaded {len(records)} records. Starting evaluation...")
    
    results = []
    
    for idx, record in enumerate(records):
        print(f"[{idx+1}/{len(records)}] Evaluating query: {record['query'][:50]}...")
        try:
            start = time.time()
            response = requests.post(api_url, json=record)
            response.raise_for_status()
            profile = response.json()
            elapsed = time.time() - start
            print(f"  -> Done in {elapsed:.2f}s. Abstention: {profile['abstention']['recommended']}")
            
            results.append({
                "request": record,
                "trust_profile": profile
            })
        except Exception as e:
            print(f"  -> Error: {e}")
            
    # Aggregate stats
    total_evals = len(results)
    total_abstentions = sum(1 for r in results if r["trust_profile"]["abstention"]["recommended"])
    
    summary = {
        "total_evaluations": total_evals,
        "total_abstentions": total_abstentions,
        "abstention_rate": total_abstentions / total_evals if total_evals > 0 else 0,
        "detailed_results": results
    }
    
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
        
    print(f"Experiment complete! Results saved to {output_path}")
    print(f"Summary: {total_abstentions}/{total_evals} abstentions recommended.")

def main():
    parser = argparse.ArgumentParser(description="Run benchmark experiments against the SearchTrust API")
    parser.add_argument("--input", type=str, required=True, help="Input adapted JSONL file")
    parser.add_argument("--api-url", type=str, default="http://localhost:8000/api/analyze", help="API Endpoint URL")
    parser.add_argument("--output", type=str, default="results/experiment_results.json", help="Output JSON results")
    args = parser.parse_args()
    
    run_experiment(args.input, args.api_url, args.output)

if __name__ == "__main__":
    main()
