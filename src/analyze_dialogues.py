import sys
import os
import json
import traceback

def audit_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {{corpus_path}}", file=sys.stderr)
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
                    errors.append((idx, "Root element is not a JSON object"))
                    continue
                
                if "dialogue" not in data and "messages" not in data:
                    errors.append((idx, "Missing dialogue or messages key"))
                    continue
                
                messages = data.get("dialogue") or data.get("messages")
                if not isinstance(messages, list) or len(messages) == 0:
                    errors.append((idx, "Dialogue turns is empty or not a list"))
                    continue
                
                valid_dialogues += 1
            except json.JSONDecodeError as jde:
                errors.append((idx, f"JSON decode error: {{str(jde)}}"))
            except Exception as e:
                errors.append((idx, f"Unexpected error: {{str(e)}}"))
                
    report = {
        "total_lines": total_lines,
        "valid_dialogues": valid_dialogues,
        "error_count": len(errors),
        "errors": errors[:50]
    }
    
    report_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/audit_report.json"
    with open(report_path, "w", encoding="utf-8") as rf:
        json.dump(report, rf, ensure_ascii=False, indent=2)
        
    print(f"Audit completed. Valid: {{valid_dialogues}}/{{total_lines}}. Report saved to {{report_path}}")

if __name__ == "__main__":
    try:
        audit_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
