import sys
import os
import traceback
import time
import json

def audit_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {{corpus_path}}", file=sys.stderr)
        sys.exit(1)

    total_lines = 0
    valid_dialogues = 0
    errors = []

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            total_lines += 1
            try:
                data = json.loads(line)
                if "dialogue" not in data or not isinstance(data["dialogue"], list):
                    errors.append(f"Line {{line_num}}: Missing 'dialogue' list")
                    continue
                
                turns = data["dialogue"]
                if len(turns) == 0:
                    errors.append(f"Line {{line_num}}: Empty dialogue turns")
                    continue

                prev_speaker = None
                turn_error = False
                for turn in turns:
                    if "speaker" not in turn or "text" not in turn:
                        errors.append(f"Line {{line_num}}: Turn missing speaker or text")
                        turn_error = True
                        break
                    current_speaker = turn["speaker"]
                    if prev_speaker and current_speaker == prev_speaker:
                        errors.append(f"Line {{line_num}}: Consecutive turns by same speaker '{{current_speaker}}'")
                    prev_speaker = current_speaker

                if not turn_error:
                    valid_dialogues += 1
            except json.JSONDecodeError as jde:
                errors.append(f"Line {{line_num}}: Invalid JSON -> {{jde}}")

    print(f"Total lines audited: {{total_lines}}")
    print(f"Valid dialogues: {{valid_dialogues}}")
    print(f"Errors detected: {{len(errors)}}")
    
    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        sys.exit(1)
    else:
        print("Audit completed successfully with zero errors.")

if __name__ == "__main__":
    try:
        audit_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
