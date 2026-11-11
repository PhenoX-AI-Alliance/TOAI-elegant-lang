import sys
import os
import traceback
import time
import json

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
        sys.exit(1)
        
    total_dialogues = 0
    valid_dialogues = 0
    errors = []
    
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            total_dialogues += 1
            try:
                data = json.loads(line)
                if "dialogue_id" not in data or "turns" not in data:
                    errors.append(f"Line {line_num}: Missing dialogue_id or turns")
                    continue
                turns = data["turns"]
                if not isinstance(turns, list) or len(turns) == 0:
                    errors.append(f"Line {line_num}: turns must be a non-empty list")
                    continue
                
                prev_role = None
                turn_error = False
                for t in turns:
                    if "role" not in t or "content" not in t:
                        errors.append(f"Line {line_num}: Turn missing role or content")
                        turn_error = True
                        break
                    current_role = t["role"]
                    if prev_role and prev_role == current_role:
                        errors.append(f"Line {line_num}: Consecutive turns with same role '{current_role}'")
                        turn_error = True
                        break
                    prev_role = current_role
                
                if not turn_error:
                    valid_dialogues += 1
            except json.JSONDecodeError as jde:
                errors.append(f"Line {line_num}: Invalid JSON - {str(jde)}")
            except Exception as e:
                errors.append(f"Line {line_num}: Unexpected error - {str(e)}")
                
    report = {
        "total_dialogues": total_dialogues,
        "valid_dialogues": valid_dialogues,
        "error_count": len(errors),
        "errors": errors
    }
    
    report_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/audit_report.json"
    with open(report_path, "w", encoding="utf-8") as rf:
        json.dump(report, rf, ensure_ascii=False, indent=2)
        
    print(f"Analysis complete. Total: {total_dialogues}, Valid: {valid_dialogues}, Errors: {len(errors)}")
    print(f"Report saved to {report_path}")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
