import sys
import os
import traceback
import time
import json

def analyze_corpus(file_path):
    if not os.path.exists(file_path):
        print(f"Error: Corpus not found at {{file_path}}")
        sys.exit(1)

    total_records = 0
    errors_found = 0
    dialogues = {}

    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                total_records += 1
                did = record.get("dialogue_id")
                if did not in dialogues:
                    dialogues[did] = []
                dialogues[did].append(record)

                if record.get("error"):
                    errors_found += 1
            except json.JSONDecodeError as e:
                print(f"JSON Decode Error at line {{line_num}}: {{e}}")

    print(f"Total Records: {{total_records}}")
    print(f"Total Dialogues: {{len(dialogues)}}")
    print(f"Total Errors Recorded: {{errors_found}}")

    for did, turns in dialogues.items():
        turns.sort(key=lambda x: x.get("turn", 0))
        expected_turn = 1
        for turn in turns:
            current_turn = turn.get("turn")
            if current_turn != expected_turn:
                print(f"Warning: Dialogue {{did}} has turn sequence mismatch. Expected {{expected_turn}}, got {{current_turn}}")
            expected_turn += 1

if __name__ == "__main__":
    corpus = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    analyze_corpus(corpus)
