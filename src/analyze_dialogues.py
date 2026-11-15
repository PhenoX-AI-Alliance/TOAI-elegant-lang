import sys
import os
import traceback
import time
import json

def audit_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    report_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/audit_report.json"
    
    results = {
        "total_lines": 0,
        "valid_records": 0,
        "errors": []
    }
    
    if not os.path.exists(corpus_path):
        results["errors"].append(f"Corpus not found at {corpus_path}")
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            results["total_lines"] += 1
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                if not isinstance(record, dict):
                    raise ValueError("Record is not a JSON object")
                if "dialogue" not in record and "messages" not in record:
                    raise KeyError("Missing dialogue or messages key")
                results["valid_records"] += 1
            except Exception as e:
                results["errors"].append({
                    "line": line_num,
                    "error": str(e)
                })

    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"Audit completed. Report saved to {report_path}")
    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    try:
        audit_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
