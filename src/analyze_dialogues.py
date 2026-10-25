import sys
import os
import traceback
import time
import json

def audit_dialogues():
    corpus_path = '/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl'
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {corpus_path}")
        sys.exit(1)
        
    total_lines = 0
    valid_lines = 0
    errors = []
    
    with open(corpus_path, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f, 1):
            total_lines += 1
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if not isinstance(data, dict):
                    raise ValueError("Row is not a JSON object")
                if "dialogue" not in data and "messages" not in data:
                    raise KeyError("Missing dialogue or messages key")
                valid_lines += 1
            except Exception as e:
                errors.append({"line": idx, "error": str(e)})
                
    report = {
        "total_lines": total_lines,
        "valid_lines": valid_lines,
        "error_count": len(errors),
        "errors": errors
    }
    
    report_dir = '/home/phenox/gemini-sandbox/TOAI_Generated'
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, 'dialogues_audit_report.json')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        
    print(f"Audit completed. Report saved to {report_path}")

if __name__ == '__main__':
    try:
        audit_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
