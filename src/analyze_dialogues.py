import sys
import os
import traceback
import time
import json

def analyze_corpus():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    report_path = "/home/phenox/gemini-sandbox/TOAI_Generated/dialogue_audit_report.json"
    
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    results = {
        "total_lines": 0,
        "valid_dialogues": 0,
        "errors": []
    }
    
    if not os.path.exists(corpus_path):
        results["errors"].append(f"Corpus file not found: {corpus_path}")
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"Warning: {corpus_path} does not exist. Empty report generated.")
        return
        
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            results["total_lines"] += 1
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if not isinstance(data, dict):
                    raise ValueError("Root element must be an object")
                if "dialogue" not in data and "messages" not in data:
                    raise ValueError("Missing dialogue or messages key")
                results["valid_dialogues"] += 1
            except Exception as e:
                results["errors"].append({
                    "line": line_num,
                    "error": str(e)
                })
                
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        
    print(f"Audit completed. Total lines: {results['total_lines']}, Valid: {results['valid_dialogues']}, Errors: {len(results['errors'])}")

if __name__ == "__main__":
    try:
        analyze_corpus()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
