import sys
import os
import traceback
import time
import json

def audit_dialogues(file_path):
    if not os.path.exists(file_path):
        print(f"Error: Corpus file not found at {file_path}")
        sys.exit(1)
        
    total_dialogues = 0
    errors = 0
    
    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            total_dialogues += 1
            try:
                data = json.loads(line)
                if "turns" not in data or not isinstance(data["turns"], list):
                    print(f"Line {line_num}: Missing 'turns' list")
                    errors += 1
                    continue
                
                expected_speaker = "user"
                for turn_idx, turn in enumerate(data["turns"]):
                    if "speaker" not in turn or "text" not in turn:
                        print(f"Line {line_num}, turn {turn_idx}: Missing speaker or text")
                        errors += 1
                        break
                    current_speaker = turn["speaker"]
                    if current_speaker != expected_speaker:
                        print(f"Line {line_num}, turn {turn_idx}: Speaker sequence violation. Expected {expected_speaker}, got {current_speaker}")
                        errors += 1
                    expected_speaker = "assistant" if expected_speaker == "user" else "user"
            except json.JSONDecodeError as e:
                print(f"Line {line_num}: Invalid JSON - {e}")
                errors += 1
                
    print(f"Audit completed. Total dialogues: {total_dialogues}, Errors found: {errors}")
    if errors > 0:
        sys.exit(1)

if __name__ == "__main__":
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    audit_dialogues(corpus_path)
