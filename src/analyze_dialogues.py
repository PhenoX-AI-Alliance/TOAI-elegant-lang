import sys
import os
import traceback
import time
import json

def audit_dialogues(corpus_path):
    if not os.path.exists(corpus_path):
        raise FileNotFoundError(f"Corpus not found at {corpus_path}")
    
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
                if d_id not in dialogues:
                    dialogues[d_id] = []
                dialogues[d_id].append(record)
            except json.JSONDecodeError:
                parse_errors += 1

    consistency_issues = 0
    for d_id, turns in dialogues.items():
        expected_speaker = "user"
        for turn in turns:
            current_speaker = turn.get("speaker")
            if current_speaker != expected_speaker:
                consistency_issues += 1
            expected_speaker = "assistant" if expected_speaker == "user" else "user"

    report = {
        "total_lines": total_lines,
        "parse_errors": parse_errors,
        "total_dialogues": len(dialogues),
        "consistency_issues": consistency_issues
    }
    return report

if __name__ == "__main__":
    corpus = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    try:
        result = audit_dialogues(corpus)
        print(json.dumps(result, indent=2))
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
