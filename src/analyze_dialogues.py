import sys
import os
import traceback
import time
import json

def analyze_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
        sys.exit(1)

    total_lines = 0
    valid_dialogues = 0
    errors = []

    with open(corpus_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, 1):
            total_lines += 1
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if not isinstance(data, dict):
                    errors.append(f"Line {idx}: Not a JSON object")
                    continue
                if "messages" not in data and "dialogue" not in data:
                    errors.append(f"Line {idx}: Missing 'messages' or 'dialogue' key")
                    continue
                valid_dialogues += 1
            except json.JSONDecodeError as e:
                errors.append(f"Line {idx}: JSON decode error - {str(e)}")

    print(f"Total lines analyzed: {total_lines}")
    print(f"Valid dialogues: {valid_dialogues}")
    print(f"Errors found: {len(errors)}")

    if errors:
        print("Detailed errors:")
        for err in errors[:10]:
            print(f" - {err}")

    report = {
        "total_lines": total_lines,
        "valid_dialogues": valid_dialogues,
        "error_count": len(errors),
        "errors": errors
    }

    report_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/analysis_report.json"
    with open(report_path, "w", encoding="utf-8") as rf:
        json.dump(report, rf, ensure_ascii=False, indent=2)
    print(f"Report saved to {report_path}")

if __name__ == "__main__":
    try:
        analyze_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
