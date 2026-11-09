import sys
import os
import traceback
import time
import json

def analyze_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {corpus_path}")
        sys.exit(1)

    total_dialogues = 0
    errors = 0

    print("Starting dialogue audit...")
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                total_dialogues += 1
                if "dialogue_id" not in data or "turns" not in data:
                    print(f"Line {line_num}: Missing required fields.")
                    errors += 1
                    continue
                turns = data["turns"]
                if not isinstance(turns, list) or len(turns) == 0:
                    print(f"Line {line_num}: Turns must be a non-empty list.")
                    errors += 1
                    continue
                expected_speaker = "user"
                for turn_idx, turn in enumerate(turns):
                    if "speaker" not in turn or "text" not in turn:
                        print(f"Line {line_num}, Turn {turn_idx}: Missing speaker or text.")
                        errors += 1
                        break
                    if turn["speaker"] != expected_speaker:
                        print(f"Line {line_num}, Turn {turn_idx}: Speaker sequence mismatch. Expected {expected_speaker}, got {turn['speaker']}.")
                        errors += 1
                    expected_speaker = "assistant" if expected_speaker == "user" else "user"
            except json.JSONDecodeError as e:
                print(f"Line {line_num}: Invalid JSON -> {e}")
                errors += 1
            except Exception as e:
                print(f"Line {line_num}: Unexpected error -> {e}")
                errors += 1

    print(f"Audit completed. Total dialogues: {total_dialogues}, Errors found: {errors}")
    if errors > 0:
        sys.exit(1)
    else:
        print("All dialogues are valid.")

if __name__ == "__main__":
    try:
        analyze_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
