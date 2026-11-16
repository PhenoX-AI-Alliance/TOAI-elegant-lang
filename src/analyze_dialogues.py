import sys
import os
import traceback
import time
import json

def audit_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {{corpus_path}}", file=sys.stderr)
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
                turn = record.get("turn")
                speaker = record.get("speaker")
                text = record.get("text")

                if d_id is None or turn is None or speaker is None or text is None:
                    parse_errors += 1
                    continue

                if d_id not in dialogues:
                    dialogues[d_id] = []
                dialogues[d_id].append({"turn": turn, "speaker": speaker, "text": text})
            except json.JSONDecodeError:
                parse_errors += 1

    consistency_issues = 0
    for d_id, turns in dialogues.items():
        turns.sort(key=lambda x: x["turn"])
        expected_turn = 1
        for t in turns:
            if t["turn"] != expected_turn:
                consistency_issues += 1
            expected_turn += 1

    report = {
        "total_lines": total_lines,
        "parse_errors": parse_errors,
        "total_dialogues": len(dialogues),
        "consistency_issues": consistency_issues,
        "status": "success" if parse_errors == 0 and consistency_issues == 0 else "warning"
    }

    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    try:
        audit_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
