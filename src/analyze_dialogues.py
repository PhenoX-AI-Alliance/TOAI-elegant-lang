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
                    errors.append((idx, "Root element is not a JSON object"))
                    continue
                if "dialogue" not in data and "messages" not in data:
                    errors.append((idx, "Missing dialogue or messages key"))
                    continue
                valid_dialogues += 1
            except json.JSONDecodeError as e:
                errors.append((idx, f"JSON Decode Error: {e}"))
                
    report = {
        "timestamp": time.time(),
        "total_lines": total_lines,
        "valid_dialogues": valid_dialogues,
        "error_count": len(errors),
        "errors": errors[:50]
    }
    
    report_dir = "/home/phenox/gemini-sandbox/TOAI_Generated"
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, "dialogue_audit_report.json")
    
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        
    print(f"Audit completed. Total: {total_lines}, Valid: {valid_dialogues}, Errors: {len(errors)}")
    print(f"Report saved to {report_path}")

if __name__ == "__main__":
    try:
        audit_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
