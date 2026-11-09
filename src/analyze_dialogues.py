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

    print(f"Starting dialogue audit for: {corpus_path}")

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            total_lines += 1
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if not isinstance(data, dict):
                    raise ValueError("Root element is not a JSON object")
                
                if "dialogue" not in data and "messages" not in data:
                    raise KeyError("Missing 'dialogue' or 'messages' key in JSON object")
                
                messages = data.get("dialogue", data.get("messages", []))
                if not isinstance(messages, list) or len(messages) == 0:
                    raise ValueError("Messages field is empty or not a list")

                for msg_idx, msg in enumerate(messages):
                    if not isinstance(msg, dict):
                        raise ValueError(f"Message at index {msg_idx} is not a dict")
                    if "role" not in msg or "content" not in msg:
                        raise KeyError(f"Message at index {msg_idx} missing 'role' or 'content'")

                valid_dialogues += 1
            except Exception as e:
                errors += 1
                error_details.append({"line": line_num, "error": str(e)})

    report = {
        "total_lines_checked": total_lines,
        "valid_dialogues": valid_dialogues,
        "error_count": errors,
        "errors": error_details,
        "timestamp": time.time()
    }

    report_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/audit_report.json"
    with open(report_path, "w", encoding="utf-8") as rf:
        json.dump(report, rf, ensure_ascii=False, indent=2)

    print(f"Audit completed. Valid: {valid_dialogues}, Errors: {errors}")
    print(f"Report saved to {report_path}")

if __name__ == "__main__":
    try:
        analyze_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
