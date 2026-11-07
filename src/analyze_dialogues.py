# -*- coding: utf-8 -*-
import sys
import os
import traceback
import time
import json

def audit_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus path not found: {corpus_path}")
        sys.exit(1)

    total_lines = 0
    errors = 0
    audit_results = []

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            total_lines += 1
            try:
                data = json.loads(line)
                if not all(k in data for k in ["dialogue_id", "speaker", "message", "response"]):
                    errors += 1
                    audit_results.append({"line": line_num, "status": "malformed_keys"})
                else:
                    audit_results.append({"line": line_num, "status": "ok", "dialogue_id": data["dialogue_id"]})
            except json.JSONDecodeError:
                errors += 1
                audit_results.append({"line": line_num, "status": "json_decode_error"})

    report = {
        "timestamp": time.time(),
        "total_lines": total_lines,
        "errors": errors,
        "results": audit_results
    }

    report_path = "/home/phenox/gemini-sandbox/TOAI_Generated/dialogue_audit_report.json"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"Audit completed successfully. Total: {total_lines}, Errors: {errors}")

if __name__ == "__main__":
    try:
        audit_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
