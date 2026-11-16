import sys
import os
import traceback
import time
import json

def audit_dialogues(corpus_path):
    print(f"Starting audit of corpus: {corpus_path}")
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus path not found: {corpus_path}")
        sys.exit(1)

    total_records = 0
    valid_records = 0
    errors = []

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            total_records += 1
            try:
                data = json.loads(line)
                if "dialogue_id" not in data:
                    errors.append(f"Line {line_num}: Missing 'dialogue_id'")
                    continue
                if "turns" not in data or not isinstance(data["turns"], list):
                    errors.append(f"Line {line_num}: Missing or invalid 'turns' field")
                    continue
                
                turns = data["turns"]
                if len(turns) == 0:
                    errors.append(f"Line {line_num}: Empty turns list")
                    continue

                turn_error = False
                for t_idx, turn in enumerate(turns):
                    if "role" not in turn or "content" not in turn:
                        errors.append(f"Line {line_num}, Turn {t_idx}: Missing 'role' or 'content'")
                        turn_error = True
                        break
                if turn_error:
                    continue

                valid_records += 1
            except json.JSONDecodeError as jde:
                errors.append(f"Line {line_num}: JSONDecodeError - {str(jde)}")
            except Exception as e:
                errors.append(f"Line {line_num}: Unexpected error - {str(e)}")

    print(f"Audit completed.")
    print(f"Total records processed: {total_records}")
    print(f"Valid records: {valid_records}")
    print(f"Error count: {len(errors)}")

    if errors:
        print("Encountered errors:")
        for err in errors[:10]:
            print(f" - {err}")
        if len(errors) > 10:
            print(f" ... and {len(errors) - 10} more errors.")
        sys.exit(1)
    else:
        print("All dialogues are structurally valid.")
        sys.exit(0)

if __name__ == "__main__":
    corpus = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    audit_dialogues(corpus)
