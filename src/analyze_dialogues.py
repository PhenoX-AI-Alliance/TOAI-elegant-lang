import sys
import os
import traceback
import time
import json

def analyze_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {{corpus_path}}", file=sys.stderr)
        sys.exit(1)

    total_lines = 0
    valid_dialogues = 0
    errors = []

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            total_lines += 1
            line_str = line.strip()
            if not line_str:
                continue
            try:
                data = json.loads(line_str)
                if not isinstance(data, dict):
                    raise ValueError("Line root must be a JSON object.")
                if "messages" not in data and "dialogue" not in data:
                    raise KeyError("Missing 'messages' or 'dialogue' key in dialogue entry.")
                valid_dialogues += 1
            except Exception as e:
                errors.append({"line": line_num, "error": str(e)})

    report = {
        "total_lines": total_lines,
        "valid_dialogues": valid_dialogues,
        "error_count": len(errors),
        "errors": errors
    }

    report_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/audit_report.json"
    with open(report_path, "w", encoding="utf-8") as rf:
        json.dump(report, rf, ensure_ascii=False, indent=2)

    print(f"Audit completed. Valid: {{valid_dialogues}}, Errors: {{len(errors)}}")
    print(f"Report saved to {{report_path}}")

if __name__ == "__main__":
    try:
        analyze_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
