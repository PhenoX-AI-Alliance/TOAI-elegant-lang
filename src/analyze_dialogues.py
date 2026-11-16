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
    valid_lines = 0
    errors = []
    
    with open(corpus_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            total_lines += 1
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if not isinstance(data, dict):
                    errors.append({"line": idx, "error": "Root element is not a JSON object"})
                    continue
                if "messages" not in data and "dialogue" not in data and "turns" not in data:
                    errors.append({"line": idx, "error": "Missing dialogue key (messages, dialogue, or turns)"})
                    continue
                valid_lines += 1
            except json.JSONDecodeError as e:
                errors.append({"line": idx, "error": f"JSONDecodeError: {str(e)}"})
            except Exception as e:
                errors.append({"line": idx, "error": f"Unexpected error: {str(e)}"})
                
    report = {
        "timestamp": time.time(),
        "total_lines": total_lines,
        "valid_lines": valid_lines,
        "error_count": len(errors),
        "errors": errors
    }
    
    report_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/reports"
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, "dialogue_audit_report.json")
    
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        
    print(f"Analysis complete. Total: {total_lines}, Valid: {valid_lines}, Errors: {len(errors)}")
    print(f"Report saved to {report_path}")

if __name__ == "__main__":
    try:
        analyze_corpus()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
