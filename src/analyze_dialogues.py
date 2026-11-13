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
            total_lines += 1
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if not isinstance(data, dict):
                    errors.append((idx, "Line is not a JSON object"))
                    continue
                if "dialogue" not in data and "messages" not in data:
                    errors.append((idx, "Missing dialogue or messages key"))
                    continue
                valid_dialogues += 1
            except json.JSONDecodeError as e:
                errors.append((idx, f"JSON decode error: {str(e)}"))
                
    result = {
        "timestamp": time.time(),
        "total_lines": total_lines,
        "valid_dialogues": valid_dialogues,
        "error_count": len(errors),
        "errors": errors[:100]
    }
    
    out_dir = "/home/phenox/gemini-sandbox/TOAI_Generated"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "dialogue_audit_report.json")
    with open(out_path, "w", encoding="utf-8") as out_f:
        json.dump(result, out_f, indent=2, ensure_ascii=False)
        
    print(f"Audit completed. Report saved to {out_path}")
    print(f"Total lines: {total_lines}, Valid: {valid_dialogues}, Errors: {len(errors)}")

if __name__ == "__main__":
    try:
        audit_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
