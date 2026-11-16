import sys
import os
import traceback
import time
import json

def audit_dialogues():
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
            total_lines += 1
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if not isinstance(data, dict):
                    errors.append({"line": idx, "error": "Root element is not a JSON object"})
                    continue
                
                if "messages" not in data and "dialogue" not in data:
                    errors.append({"line": idx, "error": "Missing 'messages' or 'dialogue' key"})
                    continue
                
                messages = data.get("messages") or data.get("dialogue")
                if not isinstance(messages, list) or len(messages) == 0:
                    errors.append({"line": idx, "error": "Messages/dialogue is not a valid non-empty list"})
                    continue
                
                valid_dialogues += 1
            except json.JSONDecodeError as e:
                errors.append({"line": idx, "error": f"JSONDecodeError: {str(e)}"})
            except Exception as e:
                errors.append({"line": idx, "error": f"Unexpected error: {str(e)}"})
                
    report = {
        "timestamp": time.time(),
        "total_lines": total_lines,
        "valid_dialogues": valid_dialogues,
        "error_count": len(errors),
        "errors": errors
    }
    
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as rf:
        json.dump(report, rf, ensure_ascii=False, indent=2)
        
    print(f"Audit completed. Total: {total_lines}, Valid: {valid_dialogues}, Errors: {len(errors)}")
    print(f"Report saved to {report_path}")

if __name__ == "__main__":
    try:
        audit_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
