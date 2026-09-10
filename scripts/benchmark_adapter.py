import json
import argparse
from pathlib import Path
import uuid
from datetime import datetime

def convert_alce_to_analyze_request(record):
    """
    Converts a mock ALCE benchmark record into our API's AnalyzeRequest schema.
    """
    # Create fake sources from the context
    sources = []
    if "context" in record and isinstance(record["context"], list):
        for idx, doc in enumerate(record["context"]):
            sources.append({
                "source_id": str(uuid.uuid4()),
                "title": doc.get("title", f"Document {idx}"),
                "content": doc.get("text", ""),
                "source_type": "PRIMARY",
                "published_at": doc.get("published_at")
            })

    return {
        "query": record.get("question", ""),
        "answer": record.get("answer", ""),
        "query_time": datetime.utcnow().isoformat() + "Z",
        "sources": sources,
        "citations": record.get("citations", [])
    }

def main():
    parser = argparse.ArgumentParser(description="Convert benchmark datasets to AnalyzeRequest format")
    parser.add_argument("--input", type=str, required=True, help="Input JSONL file")
    parser.add_argument("--output", type=str, required=True, help="Output JSONL file")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(input_path, "r", encoding="utf-8") as fin, open(output_path, "w", encoding="utf-8") as fout:
        for line in fin:
            if not line.strip():
                continue
            record = json.loads(line)
            req = convert_alce_to_analyze_request(record)
            fout.write(json.dumps(req) + "\n")
            
    print(f"Successfully converted dataset and saved to {output_path}")

if __name__ == "__main__":
    main()
