import sys
import os
import traceback
import time
import json

def audit_dialogues(corpus_path):
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {{corpus_path}}")
        sys.exit(1)

    total_lines = 0
    parse_errors = 0
    dialogue_threads = {}

    print(f"Starting audit of dialogues from {{corpus_path}}...")

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
                    print(f"Warning: Missing required fields on line {{line_num}}")
                    parse_errors += 1
                    continue

                if d_id not in dialogue_threads:
                    dialogue_threads[d_id] = []
                dialogue_threads[d_id].append({"speaker": speaker, "text": text})
            except json.JSONDecodeError as e:
                print(f"JSON decode error on line {{line_num}}: {{e}}")
                parse_errors += 1

    consistency_issues = 0
    for d_id, thread in dialogue_threads.items():
        expected_speaker = "user"
        for i, turn in enumerate(thread):
            if turn["speaker"] != expected_speaker:
                print(f"Consistency issue in dialogue {{d_id}} at turn {{i}}: Expected {{expected_speaker}}, got {{turn['speaker']}}")
                consistency_issues += 1
            expected_speaker = "assistant" if expected_speaker == "user" else "user"

    print("--- Audit Summary ---")
    print(f"Total lines processed: {{total_lines}}")
    print(f"Parse errors: {{parse_errors}}")
    print(f"Total dialogues: {{len(dialogue_threads)}}")
    print(f"Consistency issues found: {{consistency_issues}}")

    if parse_errors > 0 or consistency_issues > 0:
        print("Audit completed with warnings/errors.")
    else:
        print("Audit completed successfully with zero errors.")

if __name__ == "__main__":
    corpus = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    audit_dialogues(corpus)
