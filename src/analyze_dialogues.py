import sys
import os
import traceback
import time
import json

def analyze_corpus():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
        sys.exit(1)
        
    total_lines = 0
    valid_dialogues = 0
    errors = []
    
    with open(corpus_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            total_lines += 1
            try:
                data = json.loads(line)
                if not isinstance(data, dict):
                    raise ValueError("Root element must be a JSON object.")
                if "dialogue" not in data and "messages" not in data:
                    raise KeyError("Missing 'dialogue' or 'messages' key in JSON object.")
                valid_dialogues += 1
            except Exception as e:
                errors.append({"line": line_num, "error": str(e)})
                
    report = {
        "total_lines": total_lines,
        "valid_dialogues": valid_dialogues,
        "error_count": len(errors),
        "errors": errors
    }
    
    report_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/reports"
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, "dialogue_audit_report.json")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        
    print(f"Analysis completed. Valid: {valid_dialogues}/{total_lines}. Report saved to {report_path}")

if __name__ == "__main__":
    try:
        analyze_corpus()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
