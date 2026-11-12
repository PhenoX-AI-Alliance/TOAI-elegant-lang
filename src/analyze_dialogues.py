import sys
import os
import traceback
import time
import json

def analyze_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {{corpus_path}}", file=sys.stderr)
        sys.exit(1)

    total_lines = 0
    valid_dialogues = 0
    errors = 0
    audit_results = []

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            total_lines += 1
            line_str = line.strip()
            if not line_str:
                continue
            
            try:
                data = json.loads(line_str)
                if not isinstance(data, dict):
                    raise ValueError("JSON root must be an object")
                
                if "dialogue" not in data and "turns" not in data:
                    raise KeyError("Missing dialogue or turns key")
                
                turns = data.get("dialogue") or data.get("turns")
                if not isinstance(turns, list) or len(turns) == 0:
                    raise ValueError("Turns must be a non-empty list")

                for turn_idx, turn in enumerate(turns):
                    if not isinstance(turn, dict):
                        raise ValueError(f"Turn {{turn_idx}} must be an object")
                    if "role" not in turn or "content" not in turn:
                        raise KeyError(f"Turn {{turn_idx}} missing role or content")

                valid_dialogues += 1
                audit_results.append({"line": line_num, "status": "OK"})
            except Exception as e:
                errors += 1
                audit_results.append({"line": line_num, "status": "ERROR", "message": str(e)})

    report = {
        "timestamp": time.time(),
        "total_lines": total_lines,
        "valid_dialogues": valid_dialogues,
        "errors": errors,
        "details": audit_results
    }

    report_path = "/home/phenox/gemini-sandbox/TOAI_Generated/dialogue_audit_report.json"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as rf:
        json.dump(report, rf, ensure_ascii=False, indent=2)

    print(f"Audit completed. Total: {{total_lines}}, Valid: {{valid_dialogues}}, Errors: {{errors}}")
    print(f"Report saved to {{report_path}}")

if __name__ == "__main__":
    try:
        analyze_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
