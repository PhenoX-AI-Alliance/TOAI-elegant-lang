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
        for idx, line in enumerate(f, start=1):
            line_str = line.strip()
            if not line_str:
                continue
            total_lines += 1
            try:
                record = json.loads(line_str)
                if not isinstance(record, dict):
                    errors.append({"line": idx, "error": "Record is not a JSON object"})
                    continue
                
                if "dialogue" not in record and "messages" not in record:
                    errors.append({"line": idx, "error": "Missing dialogue or messages field"})
                    continue
                
                valid_dialogues += 1
            except json.JSONDecodeError as jde:
                errors.append({"line": idx, "error": f"JSONDecodeError: {str(jde)}"})
            except Exception as e:
                errors.append({"line": idx, "error": f"Unexpected error: {str(e)}"})
                
    report = {
        "timestamp": time.time(),
        "total_records": total_lines,
        "valid_records": valid_dialogues,
        "error_count": len(errors),
        "errors": errors
    }
    
    report_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/audit_report.json"
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
