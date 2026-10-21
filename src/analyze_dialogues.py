import sys
import os
import traceback
import time
import json

def audit_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    output_report_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/audit_report.json"
    
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
        sys.exit(1)
        
    total_lines = 0
    valid_dialogues = 0
    errors = []
    
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            total_lines += 1
            try:
                data = json.loads(line)
                if not isinstance(data, dict):
                    errors.append({"line": line_num, "error": "Root element is not a dictionary"})
                    continue
                
                if "dialogue" not in data and "messages" not in data and "turns" not in data:
                    errors.append({"line": line_num, "error": "Missing dialogue key (dialogue/messages/turns)"})
                    continue
                
                valid_dialogues += 1
            except json.JSONDecodeError as jde:
                errors.append({"line": line_num, "error": f"JSONDecodeError: {str(jde)}"})
            except Exception as e:
                errors.append({"line": line_num, "error": f"Unexpected error: {str(e)}"})
                
    report = {
        "timestamp": time.time(),
        "total_lines": total_lines,
        "valid_dialogues": valid_dialogues,
        "error_count": len(errors),
        "errors": errors
    }
    
    os.makedirs(os.path.dirname(output_report_path), exist_ok=True)
    with open(output_report_path, "w", encoding="utf-8") as out:
        json.dump(report, out, ensure_ascii=False, indent=2)
        
    print(f"Audit completed. Total: {total_lines}, Valid: {valid_dialogues}, Errors: {len(errors)}")

if __name__ == "__main__":
    try:
        audit_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
