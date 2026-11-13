import sys
import os
import traceback
import time
import json

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {corpus_path}")
        sys.exit(1)
        
    total_dialogues = 0
    errors = 0
    
    with open(corpus_path, "r", encoding="utf-8") as f:
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
                for turn in data["turns"]:
                    if "speaker" not in turn or "text" not in turn:
                        print(f"Line {line_num}: Invalid turn structure")
                        errors += 1
                        break
                    if turn["speaker"] != expected_speaker:
                        print(f"Line {line_num}: Speaker order mismatch. Expected {expected_speaker}, got {turn['speaker']}")
                        errors += 1
                    expected_speaker = "assistant" if expected_speaker == "user" else "user"
            except json.JSONDecodeError as e:
                print(f"Line {line_num}: JSON decode error: {e}")
                errors += 1
                
    print(f"Analysis complete. Total dialogues: {total_dialogues}, Errors found: {errors}")
    if errors > 0:
        sys.exit(1)

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
