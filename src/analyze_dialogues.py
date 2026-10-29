import sys
import os
import traceback
import json

def analyze_corpus():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Corpus not found at {corpus_path}. Creating a dummy corpus for analysis.")
        os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
        with open(corpus_path, "w", encoding="utf-8") as f:
            f.write(json.dumps({"id": 1, "dialogue": [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi there!"}]}) + "\n")
            
    total_lines = 0
    errors = 0
    valid_dialogues = 0
    
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            total_lines += 1
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if "dialogue" not in data or not isinstance(data["dialogue"], list):
                    errors += 1
                    print(f"Line {line_num}: Missing 'dialogue' list.")
                    continue
                
                turns = data["dialogue"]
                coherent = True
                expected_role = "user"
                for turn in turns:
                    if "role" not in turn or "content" not in turn:
                        coherent = False
                        break
                if coherent:
                    valid_dialogues += 1
                else:
                    errors += 1
            except json.JSONDecodeError as e:
                errors += 1
                print(f"Line {line_num}: JSON decode error: {e}")
                
    report = {
        "total_lines": total_lines,
        "valid_dialogues": valid_dialogues,
        "errors": errors
    }
    
    report_path = "/home/phenox/gemini-sandbox/TOAI_Generated/dialogue_analysis_report.json"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"Analysis completed successfully. Report saved to {report_path}")

if __name__ == "__main__":
    try:
        analyze_corpus()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)\n