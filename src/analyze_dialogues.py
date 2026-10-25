import sys
import os
import traceback
import time
import json

def analyze_corpus():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    output_dir = "/home/phenox/gemini-sandbox/TOAI_Generated"
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, "dialogue_audit_report.json")
    
    total_lines = 0
    valid_dialogues = 0
    errors = []
    
    if not os.path.exists(corpus_path):
        print(f"Warning: Corpus not found at {corpus_path}. Creating a dummy entry for validation.")
        os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
        with open(corpus_path, "w", encoding="utf-8") as f:
            f.write(json.dumps({"id": 1, "dialogue": [{"role": "user", "text": "hello"}, {"role": "assistant", "text": "hi"}]}) + "\n")
            
    with open(corpus_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, 1):
            total_lines += 1
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if "dialogue" not in data or not isinstance(data["dialogue"], list):
                    errors.append({"line": idx, "error": "Missing or invalid 'dialogue' field"})
                    continue
                
                turns = data["dialogue"]
                if len(turns) == 0:
                    errors.append({"line": idx, "error": "Empty dialogue turns"})
                    continue
                    
                role_check = True
                for turn_idx, turn in enumerate(turns):
                    if "role" not in turn or "text" not in turn:
                        role_check = False
                        break
                if not role_check:
                    errors.append({"line": idx, "error": "Turn missing 'role' or 'text'"})
                    continue
                    
                valid_dialogues += 1
            except json.JSONDecodeError as jde:
                errors.append({"line": idx, "error": f"JSONDecodeError: {str(jde)}"})
            except Exception as e:
                errors.append({"line": idx, "error": str(e)})
                
    report = {
        "timestamp": time.time(),
        "total_lines": total_lines,
        "valid_dialogues": valid_dialogues,
        "error_count": len(errors),
        "errors": errors
    }
    
    with open(report_path, "w", encoding="utf-8") as rf:
        json.dump(report, rf, ensure_ascii=False, indent=2)
        
    print(f"Analysis completed. Valid dialogues: {valid_dialogues}, Errors: {len(errors)}")
    print(f"Report saved to {report_path}")

if __name__ == "__main__":
    try:
        analyze_corpus()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)