import sys
import os
import traceback
import json

def analyze_corpus(corpus_file):
    print(f"Starting audit of corpus: {corpus_file}")
    if not os.path.exists(corpus_file):
        print(f"Error: Corpus file not found at {corpus_file}")
        sys.exit(1)

    total_dialogues = 0
    malformed_lines = 0
    inconsistent_turns = 0

    with open(corpus_file, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                malformed_lines += 1
                print(f"Warning: Malformed JSON at line {line_num}")
                continue

            total_dialogues += 1
            turns = data.get("turns", [])
            if not isinstance(turns, list) or len(turns) == 0:
                inconsistent_turns += 1
                print(f"Warning: Dialogue ID {data.get('dialogue_id', 'unknown')} has no valid turns.")
                continue

            expected_speaker = "user"
            for turn_idx, turn in enumerate(turns):
                speaker = turn.get("speaker")
                text = turn.get("text")
                if not speaker or not text:
                    inconsistent_turns += 1
                    print(f"Warning: Dialogue {data.get('dialogue_id')} turn {turn_idx} missing speaker or text.")

    print("Audit Complete.")
    print(f"Total dialogues processed: {total_dialogues}")
    print(f"Malformed JSON lines: {malformed_lines}")
    print(f"Inconsistent turns found: {inconsistent_turns}")

    if malformed_lines > 0 or inconsistent_turns > 0:
        print("Audit finished with warnings.")
    else:
        print("Corpus is clean and fully consistent.")

if __name__ == "__main__":
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    analyze_corpus(corpus_path)
