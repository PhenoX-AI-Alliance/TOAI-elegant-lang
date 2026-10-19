import sys
import os
import traceback
import time
import json
import toai_charter

def audit_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    report_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/audit_report.json"
    
    if not os.path.exists(corpus_path):
        print("Corpus file not found: " + corpus_path)
        sys.exit(1)
        
    total_lines = 0
    valid_dialogues = 0
    errors = []
    
    with open(corpus_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, 1):
            total_lines += 1
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if not isinstance(data, dict):
                    raise ValueError("Root element must be a JSON object")
                if "dialogue" not in data and "messages" not in data:
                    raise KeyError("Missing dialogue or messages key")
                valid_dialogues += 1
            except Exception as e:
                errors.append({"line": idx, "error": str(e)})
                
    report = {
        "timestamp": time.time(),
        "total_lines": total_lines,
        "valid_dialogues": valid_dialogues,
        "error_count": len(errors),
        "errors": errors
    }
    
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        
    print("Audit completed successfully. Report saved to " + report_path)

if __name__ == "__main__":
    try:
        audit_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
