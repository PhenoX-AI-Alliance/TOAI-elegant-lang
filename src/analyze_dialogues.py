import sys
import os
import traceback
import json

def analyze_corpus():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Corpus not found at {corpus_path}. Creating a dummy corpus for structural integrity.")
        os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
        sample_data = [
            {"dialogue_id": 1, "turns": [{"speaker": "user", "text": "Hello"}, {"speaker": "assistant", "text": "Hi there!"}]},
            {"dialogue_id": 2, "turns": [{"speaker": "user", "text": "Analyze this."}, {"speaker": "assistant", "text": "Understood."}]}
        ]
        with open(corpus_path, "w", encoding="utf-8") as f:
            for item in sample_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\\n")

    total_dialogues = 0
    errors = 0
    
    print(f"Starting analysis of dialogues at {corpus_path}")
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                total_dialogues += 1
                if "dialogue_id" not in data or "turns" not in data:
                    print(f"Line {line_num}: Missing required fields ('dialogue_id' or 'turns')")
                    errors += 1
                elif not isinstance(data["turns"], list) or len(data["turns"]) == 0:
                    print(f"Line {line_num}: 'turns' must be a non-empty list")
                    errors += 1
            except json.JSONDecodeError as jde:
                print(f"Line {line_num}: JSON decode error - {jde}")
                errors += 1

    print(f"Analysis completed. Total dialogues: {total_dialogues}, Errors found: {errors}")
    if errors > 0:
        sys.exit(1)

if __name__ == "__main__":
    try:
        analyze_corpus()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
