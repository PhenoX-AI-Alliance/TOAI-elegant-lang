import sys
import os
import traceback
import time
import json

def analyze_corpus():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus path not found: {corpus_path}")
        sys.exit(1)

    total_dialogues = 0
    errors = 0

    print("Starting dialogue audit...")
    try:
        with open(corpus_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    total_dialogues += 1
                    if "dialogue" not in data or not isinstance(data["dialogue"], list):
                        print(f"Line {line_num}: Missing 'dialogue' list field.")
                        errors += 1
                        continue
                    
                    last_speaker = None
                    for turn in data["dialogue"]:
                        if "speaker" not in turn or "text" not in turn:
                            print(f"Line {line_num}: Turn missing speaker or text.")
                            errors += 1
                        current_speaker = turn.get("speaker")
                        if last_speaker and last_speaker == current_speaker:
                            print(f"Line {line_num}: Consecutive turns by same speaker: {current_speaker}")
                            errors += 1
                        last_speaker = current_speaker
                except json.JSONDecodeError as jde:
                    print(f"Line {line_num}: Invalid JSON -> {jde}")
                    errors += 1
        print(f"Audit complete. Total dialogues: {total_dialogues}, Errors found: {errors}")
        if errors > 0:
            sys.exit(1)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    analyze_corpus()
