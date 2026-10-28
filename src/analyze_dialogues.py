import sys
import os
import json

def analyze_corpus():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI_Generated/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Corpus not found at {corpus_path}. Creating a dummy sample for audit.")
        os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
        sample_data = [
            {"dialogue_id": 1, "turns": [{"speaker": "user", "text": "Hello"}, {"speaker": "assistant", "text": "Hi there!"}]},
            {"dialogue_id": 2, "turns": [{"speaker": "user", "text": "Explain AI"}, {"speaker": "assistant", "text": "AI is..."}]}
        ]
        with open(corpus_path, "w", encoding="utf-8") as f:
            for item in sample_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

    total_dialogues = 0
    errors = 0
    
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            total_dialogues += 1
            try:
                data = json.loads(line)
                if "turns" not in data or not isinstance(data["turns"], list):
                    errors += 1
                    print(f"Line {line_num}: Missing 'turns' list.")
                else:
                    for turn in data["turns"]:
                        if "speaker" not in turn or "text" not in turn:
                            errors += 1
                            print(f"Line {line_num}: Invalid turn structure.")
            except json.JSONDecodeError as e:
                errors += 1
                print(f"Line {line_num}: JSON decode error - {e}")

    print(f"Audit completed. Total dialogues: {total_dialogues}, Errors found: {errors}")

if __name__ == "__main__":
    analyze_corpus()
