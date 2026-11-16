import sys
import os
import traceback
import time
import json

def audit_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    report_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/audit_report.json"
    
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {{corpus_path}}", file=sys.stderr)
        sys.exit(1)
        
    total_lines = 0
    valid_lines = 0
    errors = []
    
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            total_lines += 1
            line_stripped = line.strip()
            if not line_stripped:
                continue
            try:
                data = json.loads(line_stripped)
                if not isinstance(data, dict):
                    raise ValueError("Root element is not a JSON object")
                if "dialogue" not in data and "messages" not in data:
                    raise KeyError("Missing 'dialogue' or 'messages' key in JSON object")
                valid_lines += 1
            except Exception as e:
                errors.append({
                    "line": line_num,
                    "error": str(e),
                    "content": line_stripped[:100]
                })
                
    report = {
        "timestamp": time.time(),
        "total_lines": total_lines,
        "valid_lines": valid_lines,
        "error_count": len(errors),
        "errors": errors
    }
    
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as out:
        json.dump(report, out, ensure_ascii=False, indent=2)
        
    print(f"Audit completed. Total: {{total_lines}}, Valid: {{valid_lines}}, Errors: {{len(errors)}}")
    print(f"Report saved to {{report_path}}")

if __name__ == "__main__":
    try:
        audit_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
