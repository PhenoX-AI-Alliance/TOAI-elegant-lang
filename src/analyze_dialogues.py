import sys
import os
import traceback
import time
import json

def analyze_corpus():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
        sys.exit(1)

    total_dialogues = 0
    total_turns = 0
    errors = []

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                total_dialogues += 1
                if "turns" not in data or not isinstance(data["turns"], list):
                    errors.append(f"Line {line_num}: Missing 'turns' list.")
                    continue
                
                expected_role = "user"
                for turn_idx, turn in enumerate(data["turns"]):
                    total_turns += 1
                    if "role" not in turn or "content" not in turn:
                        errors.append(f"Line {line_num}, Turn {turn_idx}: Missing 'role' or 'content'.")
                        continue
                    
                    current_role = turn["role"]
                    if current_role not in ["user", "assistant"]:
                        errors.append(f"Line {line_num}, Turn {turn_idx}: Invalid role '{current_role}'.")
                    
                    if turn_idx % 2 == 0 and current_role != "user":
                        errors.append(f"Line {line_num}, Turn {turn_idx}: Expected 'user' for even turn index.")
                    elif turn_idx % 2 == 1 and current_role != "assistant":
                        errors.append(f"Line {line_num}, Turn {turn_idx}: Expected 'assistant' for odd turn index.")

            except json.JSONDecodeError as jde:
                errors.append(f"Line {line_num}: Invalid JSON format -> {jde}")

    print(f"Analysis Complete.")
    print(f"Total Dialogues: {total_dialogues}")
    print(f"Total Turns: {total_turns}")
    print(f"Total Errors Found: {len(errors)}")

    if errors:
        print("Errors:")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)
    else:
        print("All dialogues are structurally sound.")
        sys.exit(0)

if __name__ == "__main__":
    try:
        analyze_corpus()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
