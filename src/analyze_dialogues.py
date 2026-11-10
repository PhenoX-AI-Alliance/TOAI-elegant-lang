import sys
import os
import traceback
import json

def analyze_corpus():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
        sys.exit(1)

    total_lines = 0
    valid_dialogues = 0
    errors = []

    with open(corpus_path, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f, 1):
            total_lines += 1
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if not isinstance(data, dict):
                    errors.append((idx, "Root element is not a JSON object"))
                    continue
                
                if "dialogue" not in data and "turns" not in data:
                    errors.append((idx, "Missing dialogue or turns key"))
                    continue

                turns = data.get("dialogue") or data.get("turns")
                if not isinstance(turns, list) or len(turns) == 0:
                    errors.append((idx, "Turns is empty or not a list"))
                    continue

                valid_dialogues += 1
            except json.JSONDecodeError as e:
                errors.append((idx, f"JSONDecodeError: {e}"))
            except Exception as e:
                errors.append((idx, f"Unexpected error: {e}"))

    print(f"Total lines audited: {total_lines}")
    print(f"Valid dialogues: {valid_dialogues}")
    print(f"Errors encountered: {len(errors)}")

    if errors:
        print("Audit found issues:")
        for line_no, err in errors[:10]:
            print(f"Line {line_no}: {err}")
        sys.exit(1)
    else:
        print("Corpus audit passed successfully.")

if __name__ == "__main__":
    try:
        analyze_corpus()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
