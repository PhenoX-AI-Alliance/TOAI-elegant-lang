import sys
import os
import traceback
import time
import json

def audit_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {{corpus_path}}")
        sys.exit(1)

    total_records = 0
    errors = 0

    print("Starting dialogue audit...")
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            total_records += 1
            try:
                data = json.loads(line)
                if "dialogue" not in data or not isinstance(data["dialogue"], list):
                    print(f"Line {{line_num}}: Missing 'dialogue' list.")
                    errors += 1
                    continue
                
                prev_speaker = None
                for turn in data["dialogue"]:
                    if "speaker" not in turn or "text" not in turn:
                        print(f"Line {{line_num}}: Turn missing speaker or text.")
                        errors += 1
                        break
                    curr_speaker = turn["speaker"]
                    if prev_speaker and prev_speaker == curr_speaker:
                        print(f"Line {{line_num}}: Consecutive turns by same speaker ({{curr_speaker}}).")
                        errors += 1
                    prev_speaker = curr_speaker
            except json.JSONDecodeError as e:
                print(f"Line {{line_num}}: Invalid JSON -> {{e}}")
                errors += 1

    print(f"Audit complete. Total: {{total_records}}, Errors: {{errors}}")
    if errors > 0:
        sys.exit(1)

if __name__ == "__main__":
    try:
        audit_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
