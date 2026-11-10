import sys
import os
import traceback
import time
import json

def audit_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {{corpus_path}}")
        sys.exit(1)

    dialogues = {}
    total_lines = 0
    parse_errors = 0

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            total_lines += 1
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                d_id = record.get("dialogue_id")
                speaker = record.get("speaker")
                text = record.get("text")

                if d_id is None or speaker is None or text is None:
                    parse_errors += 1
                    continue

                if d_id not in dialogues:
                    dialogues[d_id] = []
                dialogues[d_id].append({"speaker": speaker, "text": text, "line": line_num})
            except json.JSONDecodeError:
                parse_errors += 1

    print(f"Total lines read: {{total_lines}}")
    print(f"Parse errors: {{parse_errors}}")
    print(f"Total dialogues found: {{len(dialogues)}}")

    consistency_issues = 0
    for d_id, turns in dialogues.items():
        expected_speaker = "user"
        for idx, turn in enumerate(turns):
            if idx == 0 and turn["speaker"] != "user":
                consistency_issues += 1
            elif idx % 2 == 0 and turn["speaker"] != "user":
                consistency_issues += 1
            elif idx % 2 == 1 and turn["speaker"] != "assistant":
                consistency_issues += 1

    print(f"Dialogue consistency issues: {{consistency_issues}}")
    if consistency_issues > 0 or parse_errors > 0:
        print("Audit completed with warnings/errors.")
        sys.exit(0)
    else:
        print("Audit completed successfully with zero issues.")
        sys.exit(0)

if __name__ == "__main__":
    try:
        audit_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
