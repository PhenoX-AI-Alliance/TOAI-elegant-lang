import sys
import os
import traceback
import time
import json

def audit_dialogues(corpus_file):
    print(f"Auditing corpus file: {corpus_file}")
    if not os.path.exists(corpus_file):
        raise FileNotFoundError(f"Corpus file not found: {corpus_file}")
    
    total_lines = 0
    errors = 0
    
    with open(corpus_file, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            total_lines += 1
            try:
                data = json.loads(line)
                if "dialogue" not in data or not isinstance(data["dialogue"], list):
                    print(f"Line {line_num}: Missing 'dialogue' list.")
                    errors += 1
                    continue
                
                prev_speaker = None
                for turn_idx, turn in enumerate(data["dialogue"]):
                    if "speaker" not in turn or "text" not in turn:
                        print(f"Line {line_num}, Turn {turn_idx}: Missing speaker or text.")
                        errors += 1
                    current_speaker = turn.get("speaker")
                    if prev_speaker and prev_speaker == current_speaker:
                        print(f"Line {line_num}, Turn {turn_idx}: Consecutive turns by same speaker '{current_speaker}'.")
                        errors += 1
                    prev_speaker = current_speaker
            except json.JSONDecodeError as jde:
                print(f"Line {line_num}: JSON decode error: {jde}")
                errors += 1

    print(f"Audit completed. Total lines checked: {total_lines}, Errors found: {errors}")
    if errors > 0:
        sys.exit(1)

if __name__ == "__main__":
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    audit_dialogues(corpus_path)
