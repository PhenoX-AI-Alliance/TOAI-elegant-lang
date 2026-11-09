import sys
import os
import traceback
import time
import json

def audit_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
        sys.exit(1)
        
    total_dialogues = 0
    error_count = 0
    audit_results = []

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            total_dialogues += 1
            try:
                data = json.loads(line)
                if "dialogue_id" not in data or "turns" not in data:
                    raise ValueError(f"Missing required keys in line {line_num}")
                
                turns = data["turns"]
                if not isinstance(turns, list) or len(turns) == 0:
                    raise ValueError(f"Invalid or empty turns in dialogue {data.get('dialogue_id', line_num)}")
                
                expected_role = "user"
                for turn_idx, turn in enumerate(turns):
                    if "role" not in turn or "content" not in turn:
                        raise ValueError(f"Turn {turn_idx} missing role or content in dialogue {data.get('dialogue_id')}")
                    if turn["role"] != expected_role:
                        raise ValueError(f"Role mismatch in dialogue {data.get('dialogue_id')} at turn {turn_idx}: expected {expected_role}, got {turn['role']}")
                    expected_role = "assistant" if expected_role == "user" else "user"
                
                audit_results.append({"dialogue_id": data["dialogue_id"], "status": "OK"})
            except Exception as e:
                error_count += 1
                audit_results.append({"line": line_num, "status": "ERROR", "message": str(e)})

    report = {
        "timestamp": time.time(),
        "total_dialogues": total_dialogues,
        "error_count": error_count,
        "results": audit_results
    }
    
    report_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/audit_report.json"
    with open(report_path, "w", encoding="utf-8") as rf:
        json.dump(report, rf, ensure_ascii=False, indent=2)
    print(f"Audit completed. Total: {total_dialogues}, Errors: {error_count}. Report saved to {report_path}")

if __name__ == "__main__":
    try:
        audit_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
