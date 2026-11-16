import sys
import os
import traceback
import time
import json

def analyze_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    report_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/audit_report.json"
    
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {corpus_path}")
        sys.exit(1)
        
    total_lines = 0
    valid_dialogues = 0
    errors = []
    
    with open(corpus_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            total_lines += 1
            try:
                data = json.loads(line)
                if not isinstance(data, dict):
                    raise ValueError("Root element is not a JSON object")
                
                if "dialogue" not in data and "turns" not in data:
                    raise KeyError("Missing dialogue or turns key")
                
                turns = data.get("dialogue", data.get("turns", []))
                if not isinstance(turns, list) or len(turns) == 0:
                    raise ValueError("Turns must be a non-empty list")
                
                for t_idx, turn in enumerate(turns):
                    if not isinstance(turn, dict):
                        raise ValueError(f"Turn {t_idx} is not a valid object")
                    if "role" not in turn or "content" not in turn:
                        raise KeyError(f"Turn {t_idx} missing role or content")
                
                valid_dialogues += 1
            except Exception as e:
                errors.append({
                    "line_number": idx,
                    "error": str(e)
                })
                
    report = {
        "timestamp": time.time(),
        "total_lines_checked": total_lines,
        "valid_dialogues": valid_dialogues,
        "error_count": len(errors),
        "errors": errors
    }
    
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        
    print(f"Audit completed. Valid: {valid_dialogues}/{total_lines}. Report saved to {report_path}")

if __name__ == "__main__":
    try:
        analyze_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)\n