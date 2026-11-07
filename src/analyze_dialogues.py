import sys
import os
import traceback
import json

def audit_dialogues(corpus_path):
    print(f"Auditing corpus at: {corpus_path}")
    if not os.path.exists(corpus_path):
        print("Error: Corpus file not found.")
        sys.exit(1)

    total_records = 0
    error_records = 0

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            total_records += 1
            try:
                data = json.loads(line)
                if "dialogue" not in data or not isinstance(data["dialogue"], list):
                    print(f"Line {line_num}: Missing 'dialogue' list field.")
                    error_records += 1
                    continue
                
                prev_role = None
                for turn in data["dialogue"]:
                    if "role" not in turn or "content" not in turn:
                        print(f"Line {line_num}: Turn missing 'role' or 'content'.")
                        error_records += 1
                        break
                    current_role = turn["role"]
                    if prev_role and prev_role == current_role:
                        print(f"Line {line_num}: Consecutive identical roles detected ({current_role}).")
                    prev_role = current_role
            except json.JSONDecodeError as e:
                print(f"Line {line_num}: JSON decode error - {e}")
                error_records += 1

    print(f"Audit completed. Total: {total_records}, Errors: {error_records}")
    if error_records > 0:
        sys.exit(1)

if __name__ == "__main__":
    corpus = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    audit_dialogues(corpus)
