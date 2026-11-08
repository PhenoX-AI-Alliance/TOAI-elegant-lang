import sys
import os
import traceback
import json

def analyze_corpus():
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
                turn = record.get("turn")
                speaker = record.get("speaker")
                text = record.get("text")

                if d_id is None or turn is None or speaker is None or text is None:
                    parse_errors += 1
                    continue

                if d_id not in dialogues:
                    dialogues[d_id] = []
                dialogues[d_id].append((turn, speaker, text))
            except json.JSONDecodeError:
                parse_errors += 1

    consistency_errors = 0
    for d_id, turns in dialogues.items():
        turns.sort(key=lambda x: x[0])
        expected_turn = 1
        expected_speaker = "user"
        for turn, speaker, text in turns:
            if turn != expected_turn:
                consistency_errors += 1
            if speaker != expected_speaker:
                consistency_errors += 1
            expected_turn += 1
            expected_speaker = "assistant" if expected_speaker == "user" else "user"

    print(f"Total lines audited: {{total_lines}}")
    print(f"Parse errors: {{parse_errors}}")
    print(f"Dialogue consistency errors: {{consistency_errors}}")
    print("Dialogue audit completed successfully.")

if __name__ == "__main__":
    try:
        analyze_corpus()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
