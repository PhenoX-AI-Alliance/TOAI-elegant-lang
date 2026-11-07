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
    errors = 0
    error_details = []

    print(f"Starting analysis of dialogue corpus: {corpus_path}")

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            total_lines += 1
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if not isinstance(data, dict):
                    raise ValueError("JSON root must be an object.")
                
                if "messages" not in data and "dialogue" not in data and "turns" not in data:
                    raise KeyError("Missing required dialogue keys (messages/dialogue/turns).")

                valid_dialogues += 1
            except Exception as e:
                errors += 1
                error_details.append({"line": line_num, "error": str(e)})

    report = {
        "timestamp": time.time(),
        "total_lines": total_lines,
        "valid_dialogues": valid_dialogues,
        "errors": errors,
        "error_details": error_details
    }

    report_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/analysis_report.json"
    with open(report_path, "w", encoding="utf-8") as rf:
        json.dump(report, rf, ensure_ascii=False, indent=2)

    print(f"Analysis completed. Total: {total_lines}, Valid: {valid_dialogues}, Errors: {errors}")
    print(f"Report saved to {report_path}")

if __name__ == "__main__":
    try:
        analyze_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
