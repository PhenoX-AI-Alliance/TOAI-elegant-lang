import sys
import os
import traceback
import time
import json

def audit_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
        sys.exit(1)
        
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
                    print(f"Dialogue {data.get('dialogue_id')}: 'turns' must be a non-empty list")
                    errors += 1
                    continue
                
                expected_speaker = "user"
                for t_idx, turn in enumerate(turns):
                    if "speaker" not in turn or "text" not in turn:
                        print(f"Dialogue {data.get('dialogue_id')}, turn {t_idx}: Missing 'speaker' or 'text'")
                        errors += 1
                        break
                    
                    if turn["speaker"] != expected_speaker:
                        print(f"Dialogue {data.get('dialogue_id')}, turn {t_idx}: Unexpected speaker sequence. Expected {expected_speaker}, got {turn['speaker']}")
                        errors += 1
                    
                    expected_speaker = "assistant" if expected_speaker == "user" else "user"
                    
            except json.JSONDecodeError as e:
                print(f"Line {line_num}: JSON decode error - {e}")
                errors += 1
            except Exception as e:
                print(f"Line {line_num}: Unexpected error - {e}")
                errors += 1
                
    print(f"Audit complete. Total dialogues: {total_dialogues}, Errors found: {errors}")
    if errors > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    audit_dialogues()
