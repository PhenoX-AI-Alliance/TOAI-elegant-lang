import sys
import os
import traceback
import time
import json

def analyze_corpus():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {corpus_path}")
        sys.exit(1)

    total_lines = 0
    valid_dialogues = 0
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
                    raise ValueError("Root element must be a JSON object.")
                if "messages" not in data or not isinstance(data["messages"], list):
                    raise ValueError("Missing 'messages' list in dialogue entry.")
                
                messages = data["messages"]
                if len(messages) == 0:
                    raise ValueError("Dialogue messages list is empty.")

                for msg in messages:
                    if not isinstance(msg, dict) or "role" not in msg or "content" not in msg:
                        raise ValueError("Invalid message structure.")

                valid_dialogues += 1
            except Exception as e:
                errors += 1
                print(f"Line {line_num} audit error: {e}")

    print(f"Audit Complete. Total: {total_lines}, Valid: {valid_dialogues}, Errors: {errors}")
    if errors > 0:
        sys.exit(1)

if __name__ == "__main__":
    try:
        analyze_corpus()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
