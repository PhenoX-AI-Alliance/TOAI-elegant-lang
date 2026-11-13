# -*- coding: utf-8 -*-
import sys
import os
import traceback
import time
import json

def analyze_corpus():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
        sys.exit(1)

    total_lines = 0
    valid_dialogues = 0
    errors = 0
    audit_results = []

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            total_lines += 1
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if not isinstance(data, dict):
                    raise ValueError("Root element must be a JSON object")
                
                if "dialogue" not in data and "messages" not in data:
                    raise ValueError("Missing dialogue or messages key")
                
                messages = data.get("dialogue") or data.get("messages")
                if not isinstance(messages, list) or len(messages) == 0:
                    raise ValueError("Messages must be a non-empty list")
                
                for m_idx, msg in enumerate(messages):
                    if not isinstance(msg, dict):
                        raise ValueError(f"Message {m_idx} must be an object")
                    if "role" not in msg or "content" not in msg:
                        raise ValueError(f"Message {m_idx} missing role or content")

                valid_dialogues += 1
                audit_results.append({"line": line_num, "status": "OK"})
            except Exception as e:
                errors += 1
                audit_results.append({"line": line_num, "status": "ERROR", "reason": str(e)})

    report = {
        "total_lines": total_lines,
        "valid_dialogues": valid_dialogues,
        "errors": errors,
        "details": audit_results
    }

    report_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/audit_report.json"
    with open(report_path, "w", encoding="utf-8") as out:
        json.dump(report, out, indent=2, ensure_ascii=False)
    print(f"Audit completed. Report saved to {report_path}")

if __name__ == "__main__":
    try:
        analyze_corpus()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
