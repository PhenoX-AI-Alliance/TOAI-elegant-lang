import sys
import os
import traceback
import time
import json

def audit_dialogues(corpus_path):
    print(f"Auditing corpus at: {corpus_path}")
    if not os.path.exists(corpus_path):
        raise FileNotFoundError(f"Corpus file not found: {corpus_path}")
        
    total_dialogues = 0
    errors = 0
    
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                total_dialogues += 1
                if "dialogue_id" not in data or "turns" not in data:
                    print(f"Line {line_num}: Missing required fields ('dialogue_id' or 'turns')")
                    errors += 1
                    continue
                turns = data["turns"]
                if not isinstance(turns, list) or len(turns) == 0:
                    print(f"Line {line_num}: 'turns' must be a non-empty list")
                    errors += 1
                    continue
                expected_speaker = "user"
                for turn_idx, turn in enumerate(turns):
                    if "speaker" not in turn or "text" not in turn:
                        print(f"Line {line_num}, Turn {turn_idx}: Missing 'speaker' or 'text'")
                        errors += 1
                        break
                    if turn["speaker"] != expected_speaker:
                        print(f"Line {line_num}, Turn {turn_idx}: Speaker mismatch. Expected {expected_speaker}, got {turn['speaker']}")
                        errors += 1
                    expected_speaker = "assistant" if expected_speaker == "user" else "user"
            except json.JSONDecodeError as jde:
                print(f"Line {line_num}: JSON decode error: {jde}")
                errors += 1
            except Exception as e:
                print(f"Line {line_num}: Unexpected error: {e}")
                errors += 1
                
    print(f"Audit complete. Total dialogues: {total_dialogues}, Errors found: {errors}")
    return errors

if __name__ == "__main__":
    corpus_file = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    try:
        err_count = audit_dialogues(corpus_file)
        if err_count > 0:
            sys.exit(1)
        else:
            sys.exit(0)
    except Exception as ex:
        traceback.print_exc()
        sys.exit(1)
