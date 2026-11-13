# -*- coding: utf-8 -*-
import sys
import os
import traceback
import time
import json

def audit_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
        sys.exit(1)

    total_lines = 0
    valid_dialogues = 0
    errors = []

    with open(corpus_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, 1):
            line_str = line.strip()
            if not line_str:
                continue
            total_lines += 1
            try:
                data = json.loads(line_str)
                if not isinstance(data, dict):
                    raise ValueError("Root element is not a JSON object")
                
                if "messages" not in data:
                    raise KeyError("Missing 'messages' key")
                
                messages = data["messages"]
                if not isinstance(messages, list) or len(messages) == 0:
                    raise ValueError("'messages' must be a non-empty list")
                
                for m_idx, msg in enumerate(messages):
                    if not isinstance(msg, dict):
                        raise ValueError(f"Message at index {m_idx} is not an object")
                    if "role" not in msg or "content" not in msg:
                        raise ValueError(f"Message at index {m_idx} missing 'role' or 'content'")
                
                valid_dialogues += 1
            except Exception as e:
                errors.append({"line": idx, "error": str(e)})

    report = {
        "timestamp": time.time(),
        "total_lines": total_lines,
        "valid_dialogues": valid_dialogues,
        "error_count": len(errors),
        "errors": errors
    }

    report_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/audit_report.json"
    with open(report_path, "w", encoding="utf-8") as out:
        json.dump(report, out, ensure_ascii=False, indent=2)

    print(f"Audit completed. Total: {total_lines}, Valid: {valid_dialogues}, Errors: {len(errors)}")
    print(f"Report saved to {report_path}")

if __name__ == "__main__":
    try:
        audit_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
