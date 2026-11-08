import sys
import os
import json
import traceback

def audit_dialogues(corpus_file):
    print(f"Auditing corpus from: {corpus_file}")
    if not os.path.exists(corpus_file):
        print(f"Error: Corpus file not found at {corpus_file}")
        sys.exit(1)

    dialogues = {}
    total_lines = 0
    parse_errors = 0

    with open(corpus_file, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            total_lines += 1
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                d_id = record.get("dialogue_id")
                if d_id not in dialogues:
                    dialogues[d_id] = []
                dialogues[d_id].append(record)
            except json.JSONDecodeError:
                parse_errors += 1

    print(f"Total lines read: {total_lines}")
    print(f"JSON parse errors: {parse_errors}")
    print(f"Total unique dialogues: {len(dialogues)}")

    integrity_issues = 0
    for d_id, turns in dialogues.items():
        sorted_turns = sorted(turns, key=lambda x: x.get("turn", 0))
        expected_turn = 1
        for turn in sorted_turns:
            current_turn = turn.get("turn")
            if current_turn != expected_turn:
                print(f"Warning: Dialogue {d_id} has turn gap. Expected {expected_turn}, got {current_turn}")
                integrity_issues += 1
            expected_turn += 1

    print(f"Integrity issues found: {integrity_issues}")
    if integrity_issues > 0:
        print("Audit completed with warnings.")
    else:
        print("Audit completed successfully with zero integrity issues.")

if __name__ == "__main__":
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    audit_dialogues(corpus_path)
