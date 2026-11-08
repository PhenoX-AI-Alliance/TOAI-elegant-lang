import sys
import os
import traceback
import time
import json

def audit_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {corpus_path}")
        sys.exit(1)

    dialogues = {}
    total_lines = 0
    malformed_lines = 0

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            total_lines += 1
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                d_id = data.get("dialogue_id")
                if d_id is None:
                    malformed_lines += 1
                    continue
                if d_id not in dialogues:
                    dialogues[d_id] = []
                dialogues[d_id].append(data)
            except json.JSONDecodeError:
                malformed_lines += 1

    print(f"Total lines read: {total_lines}")
    print(f"Malformed lines: {malformed_lines}")
    print(f"Unique dialogue sessions: {len(dialogues)}")

    errors = 0
    for d_id, turns in dialogues.items():
        if not turns:
            errors += 1
            continue
        expected_speaker = "user"
        for i, turn in enumerate(turns):
            speaker = turn.get("speaker")
            if i % 2 == 0:
                if speaker != "user":
                    errors += 1
            else:
                if speaker != "assistant":
                    errors += 1

    print(f"Dialogue consistency errors detected: {errors}")
    if errors > 0:
        print("Audit failed due to structural inconsistencies.")
        sys.exit(1)
    else:
        print("Audit completed successfully with zero errors.")

if __name__ == "__main__":
    try:
        audit_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
