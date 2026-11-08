import sys
import os
import traceback
import json

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {corpus_path}")
        sys.exit(1)
        
    total_dialogues = 0
    total_turns = 0
    errors = 0
    
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                total_dialogues += 1
                if "turns" not in data or not isinstance(data["turns"], list):
                    errors += 1
                    print(f"Line {line_num}: Missing 'turns' list")
                    continue
                for turn in data["turns"]:
                    if "speaker" not in turn or "text" not in turn:
                        errors += 1
                        print(f"Line {line_num}: Invalid turn structure")
                    total_turns += 1
            except json.JSONDecodeError as e:
                errors += 1
                print(f"Line {line_num}: JSON decode error - {e}")
                
    print(f"Analysis complete. Dialogues: {total_dialogues}, Turns: {total_turns}, Errors: {errors}")
    if errors > 0:
        sys.exit(1)

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
