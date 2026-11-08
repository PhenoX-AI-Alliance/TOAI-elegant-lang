import sys
import os
import traceback
import json

def audit_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
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
                record = json.loads(line)
                if "dialogue" not in record:
                    print(f"Line {line_num}: Missing 'dialogue' key.")
                    errors += 1
                    continue
                
                dialogue = record["dialogue"]
                if not isinstance(dialogue, list) or len(dialogue) == 0:
                    print(f"Line {line_num}: 'dialogue' must be a non-empty list.")
                    errors += 1
                    continue

                prev_speaker = None
                for turn_idx, turn in enumerate(dialogue):
                    if not isinstance(turn, dict) or "speaker" not in turn or "text" not in turn:
                        print(f"Line {line_num}, Turn {turn_idx}: Invalid turn structure.")
                        errors += 1
                        break
                    current_speaker = turn["speaker"]
                    if prev_speaker and current_speaker == prev_speaker:
                        print(f"Line {line_num}, Turn {turn_idx}: Consecutive turns by same speaker ({current_speaker}).")
                        errors += 1
                    prev_speaker = current_speaker

            except json.JSONDecodeError as e:
                print(f"Line {line_num}: Invalid JSON format: {e}")
                errors += 1

    print(f"Audit completed. Total records: {total_records}, Errors found: {errors}")
    if errors > 0:
        sys.exit(1)
    else:
        print("All dialogues are valid and well-formed.")

if __name__ == "__main__":
    try:
        audit_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
