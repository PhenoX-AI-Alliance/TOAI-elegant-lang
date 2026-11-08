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

    dialogues = {}
    total_lines = 0
    parse_errors = 0

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            total_lines += 1
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                d_id = record.get("dialogue_id")
                if d_id is None:
                    parse_errors += 1
                    continue
                if d_id not in dialogues:
                    dialogues[d_id] = []
                dialogues[d_id].append(record)
            except json.JSONDecodeError:
                parse_errors += 1

    print(f"Total lines read: {total_lines}")
    print(f"Parse errors: {parse_errors}")
    print(f"Unique dialogues found: {len(dialogues)}")

    consistency_issues = 0
    for d_id, turns in dialogues.items():
        sorted_turns = sorted(turns, key=lambda x: x.get("turn", 0))
        expected_turn = 1
        for t in sorted_turns:
            if t.get("turn") != expected_turn:
                consistency_issues += 1
            expected_turn += 1

    print(f"Consistency issues found: {consistency_issues}")
    report = {
        "total_lines": total_lines,
        "parse_errors": parse_errors,
        "unique_dialogues": len(dialogues),
        "consistency_issues": consistency_issues,
        "timestamp": time.time()
    }
    report_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/audit_report.json"
    with open(report_path, "w", encoding="utf-8") as rf:
        json.dump(report, rf, ensure_ascii=False, indent=2)
    print(f"Audit report successfully saved to {report_path}")

if __name__ == "__main__":
    try:
        audit_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
