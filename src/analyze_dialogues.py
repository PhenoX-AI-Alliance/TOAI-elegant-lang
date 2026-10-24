import sys
import os
import json
import traceback

def audit_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
        sys.exit(1)
        
    total_lines = 0
    valid_lines = 0
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
                    raise ValueError("JSON root must be an object")
                if "dialogue" not in data and "messages" not in data:
                    raise ValueError("Missing dialogue or messages key")
                valid_lines += 1
            except Exception as e:
                errors.append({"line": idx, "error": str(e)})
                
    report = {
        "total_lines": total_lines,
        "valid_lines": valid_lines,
        "error_count": len(errors),
        "errors": errors
    }
    
    output_dir = "/home/phenox/gemini-sandbox/TOAI_Generated"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "dialogue_audit_report.json")
    
    with open(output_path, "w", encoding="utf-8") as out_f:
        json.dump(report, out_f, ensure_ascii=False, indent=2)
        
    print(f"Audit completed. Report saved to {output_path}")

if __name__ == "__main__":
    try:
        audit_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
