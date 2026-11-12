import sys
import os
import traceback
import time
import json

def audit_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    print(f"Reading corpus from: {corpus_path}")
    
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
        sys.exit(1)
        
    total_lines = 0
    valid_dialogues = 0
    errors = 0
    
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            total_lines += 1
            try:
                data = json.loads(line)
                if not isinstance(data, dict):
                    raise ValueError("Root element is not a JSON object")
                
                if "messages" not in data and "dialogue" not in data and "turns" not in data:
                    raise KeyError("Missing dialogue turns field")
                
                valid_dialogues += 1
            except Exception as e:
                errors += 1
                print(f"Syntax/Schema error at line {line_num}: {e}")
                
    print(f"Audit Complete. Total: {total_lines}, Valid: {valid_dialogues}, Errors: {errors}")
    
    report = {
        "timestamp": time.time(),
        "total_lines": total_lines,
        "valid_dialogues": valid_dialogues,
        "errors": errors
    }
    
    report_path = "/home/phenox/gemini-sandbox/TOAI_Generated/dialogue_audit_report.json"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as rf:
        json.dump(report, rf, indent=2)
    print(f"Report saved to {report_path}")

if __name__ == "__main__":
    try:
        audit_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
