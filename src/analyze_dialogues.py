import sys
import os
import traceback
import time
import json

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
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
                    errors.append(f"Line {line_num}: Missing required fields ('dialogue_id' or 'turns')")
                    continue
                turns = data["turns"]
                if not isinstance(turns, list) or len(turns) == 0:
                    errors.append(f"Line {line_num}: 'turns' must be a non-empty list")
                    continue
                
                valid_sequence = True
                expected_role = "user"
                for turn_idx, turn in enumerate(turns):
                    if "role" not in turn or "content" not in turn:
                        errors.append(f"Line {line_num}, Turn {turn_idx}: Missing 'role' or 'content'")
                        valid_sequence = False
                        break
                if valid_sequence:
                    valid_dialogues += 1
            except json.JSONDecodeError as e:
                errors.append(f"Line {line_num}: Invalid JSON - {e}")
                
    report = {
        "timestamp": time.time(),
        "total_dialogues": total_dialogues,
        "valid_dialogues": valid_dialogues,
        "error_count": len(errors),
        "errors": errors
    }
    
    report_path = "/home/phenox/gemini-sandbox/TOAI_Generated/dialogue_audit_report.json"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        
    print(f"Audit completed. Total: {total_dialogues}, Valid: {valid_dialogues}, Errors: {len(errors)}")
    print(f"Report saved to {report_path}")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
