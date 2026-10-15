import sys
import os
import traceback
import time
import json

def audit_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus path not found: {corpus_path}")
        sys.exit(1)
        
    total_lines = 0
    valid_lines = 0
    errors = 0
    
    print(f"Starting dialogue audit from: {corpus_path}")
    try:
        with open(corpus_path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                total_lines += 1
                try:
                    data = json.loads(line)
                    if "dialogue" in data or ("user" in data and "assistant" in data):
                        valid_lines += 1
                    else:
                        errors += 1
                except json.JSONDecodeError:
                    errors += 1
                    
        print(f"Audit completed.")
        print(f"Total dialogues checked: {total_lines}")
        print(f"Valid dialogues: {valid_lines}")
        print(f"Malformed or invalid dialogues: {errors}")
        
    except Exception as e:
        print(f"An error occurred during auditing: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    audit_dialogues()
