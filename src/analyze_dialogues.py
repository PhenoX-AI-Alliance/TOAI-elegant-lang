import sys
import os
import traceback
import json

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI_Generated/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        alt_corpus = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
        if os.path.exists(alt_corpus):
            corpus_path = alt_corpus
        else:
            print("Error: corpus/dialogues.jsonl not found.")
            sys.exit(1)
            
    total_lines = 0
    valid_lines = 0
    errors = 0
    
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            total_lines += 1
            try:
                data = json.loads(line)
                if not isinstance(data, dict):
                    raise ValueError("Root element must be an object")
                if "dialogue" not in data and "messages" not in data:
                    raise ValueError("Missing dialogue or messages key")
                valid_lines += 1
            except Exception as e:
                errors += 1
                print(f"Line {line_num} error: {e}")
                
    print(f"Total dialogues: {total_lines}")
    print(f"Valid dialogues: {valid_lines}")
    print(f"Errors detected: {errors}")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
