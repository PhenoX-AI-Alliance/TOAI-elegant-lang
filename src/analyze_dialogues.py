import sys
import os
import traceback
import time
import json

def audit_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    output_report = "/home/phenox/gemini-sandbox/TOAI_Generated/dialogue_audit_report.json"
    
    os.makedirs(os.path.dirname(output_report), exist_ok=True)
    
    total_lines = 0
    valid_lines = 0
    errors = []
    
    if not os.path.exists(corpus_path):
        print(f"Warning: Corpus not found at {corpus_path}. Creating a dummy sample for verification.")
        os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
        with open(corpus_path, "w", encoding="utf-8") as f:
            f.write(json.dumps({"dialogue_id": 1, "turns": [{"speaker": "user", "text": "hello"}, {"speaker": "assistant", "text": "hi"}]}) + "\n")
            
    with open(corpus_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, 1):
            total_lines += 1
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if "turns" not in data or not isinstance(data["turns"], list):
                    errors.append({"line": idx, "error": "Missing 'turns' list"})
                    continue
                
                valid_turn_sequence = True
                expected_speaker = "user"
                for turn_idx, turn in enumerate(data["turns"]):
                    if "speaker" not in turn or "text" not in turn:
                        valid_turn_sequence = False
                        errors.append({"line": idx, "error": f"Turn {turn_idx} missing speaker or text"})
                        break
                if valid_turn_sequence:
                    valid_lines += 1
            except json.JSONDecodeError as jde:
                errors.append({"line": idx, "error": f"JSONDecodeError: {str(jde)}"})
                
    report = {
        "timestamp": time.time(),
        "total_lines": total_lines,
        "valid_lines": valid_lines,
        "error_count": len(errors),
        "errors": errors
    }
    
    with open(output_report, "w", encoding="utf-8") as out:
        json.dump(report, out, ensure_ascii=False, indent=2)
        
    print(f"Audit completed. Report saved to {output_report}")

if __name__ == "__main__":
    try:
        audit_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
