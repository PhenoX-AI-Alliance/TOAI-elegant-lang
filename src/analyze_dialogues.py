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
            try:
                data = json.loads(line)
                total_dialogues += 1
                if "turns" not in data or not isinstance(data["turns"], list):
                    print(f"Audit Warning: Line {line_num} missing 'turns' list.")
                    errors += 1
                else:
                    for t_idx, turn in enumerate(data["turns"]):
                        if "speaker" not in turn or "text" not in turn:
                            print(f"Audit Warning: Line {line_num}, turn {t_idx} missing speaker or text.")
                            errors += 1
            except json.JSONDecodeError as jde:
                print(f"Audit Error: Line {line_num} JSON decode failed: {jde}")
                errors += 1
                
    print(f"Audit Complete. Total Dialogues: {total_dialogues}, Errors Found: {errors}")
    if errors > 0:
        sys.exit(1)

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
