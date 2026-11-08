import sys
import os
import traceback
import time
import json

def audit_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
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
                    print(f"Line {line_num}: Missing 'turns' list.")
                    errors += 1
                    continue
                
                last_role = None
                for turn in data["turns"]:
                    if "role" not in turn or "content" not in turn:
                        print(f"Line {line_num}: Turn missing 'role' or 'content'.")
                        errors += 1
                        break
                    current_role = turn["role"]
                    if current_role == last_role:
                        print(f"Line {line_num}: Consecutive turns with the same role ({current_role}).")
                        errors += 1
                    last_role = current_role
            except json.JSONDecodeError as e:
                print(f"Line {line_num}: Invalid JSON - {e}")
                errors += 1

    print(f"Audit completed. Total dialogues: {total_dialogues}, Errors found: {errors}")
    if errors > 0:
        sys.exit(1)

if __name__ == "__main__":
    try:
        audit_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
