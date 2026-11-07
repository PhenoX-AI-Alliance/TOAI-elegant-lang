import sys
import os
import traceback
import time
import json

def analyze_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus path not found: {corpus_path}")
        sys.exit(1)

    total_dialogues = 0
    malformed_lines = 0
    audit_results = []

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                total_dialogues += 1
                dialogue = record.get("dialogue", [])
                if not isinstance(dialogue, list) or len(dialogue) == 0:
                    malformed_lines += 1
                    audit_results.append({"line": line_num, "error": "Invalid dialogue structure"})
                else:
                    for turn in dialogue:
                        if "speaker" not in turn or "text" not in turn:
                            malformed_lines += 1
                            audit_results.append({"line": line_num, "error": "Missing speaker or text in turn"})
                            break
            except json.JSONDecodeError:
                malformed_lines += 1
                audit_results.append({"line": line_num, "error": "JSON decode error"})

    report = {
        "timestamp": time.time(),
        "total_dialogues": total_dialogues,
        "malformed_lines": malformed_lines,
        "audit_results": audit_results
    }

    report_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/audit_report.json"
    with open(report_path, "w", encoding="utf-8") as rf:
        json.dump(report, rf, ensure_ascii=False, indent=2)

    print(f"Audit completed. Total: {total_dialogues}, Malformed: {malformed_lines}")
    print(f"Report saved to {report_path}")

if __name__ == "__main__":
    try:
        analyze_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
