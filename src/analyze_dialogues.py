import sys
import os
import traceback
import time
import json

def audit_dialogues(corpus_path):
    print(f"Starting dialogue audit for: {corpus_path}")
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
        sys.exit(1)
        
    total_lines = 0
    valid_lines = 0
    errors = []
    
    with open(corpus_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            total_lines += 1
            line_str = line.strip()
            if not line_str:
                continue
            try:
                data = json.loads(line_str)
                if not isinstance(data, dict):
                    raise ValueError("JSON root must be an object")
                if "dialogue" not in data and "messages" not in data:
                    raise KeyError("Missing dialogue or messages key")
                valid_lines += 1
            except Exception as e:
                errors.append({"line": idx, "error": str(e)})
                
    print(f"Audit complete. Total lines: {total_lines}, Valid: {valid_lines}, Errors: {len(errors)}")
    if errors:
        print("Encountered errors during audit:")
        for err in errors[:10]:
            print(f"Line {err['line']}: {err['error']}")
    return {"total": total_lines, "valid": valid_lines, "errors": len(errors)}

if __name__ == "__main__":
    try:
        corpus = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
        audit_dialogues(corpus)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
