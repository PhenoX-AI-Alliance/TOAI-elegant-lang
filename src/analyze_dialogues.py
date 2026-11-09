import sys
import os
import traceback
import time
import json

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {corpus_path}")
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
                data = json.loads(line)
                d_id = data.get("dialogue_id")
                if d_id is None:
                    parse_errors += 1
                    continue
                if d_id not in dialogues:
                    dialogues[d_id] = []
                dialogues[d_id].append(data)
            except json.JSONDecodeError:
                parse_errors += 1

    consistency_issues = 0
    for d_id, turns in dialogues.items():
        turns.sort(key=lambda x: x.get("turn", 0))
        expected_turn = 1
        for turn in turns:
            if turn.get("turn") != expected_turn:
                consistency_issues += 1
            expected_turn += 1

    report = {
        "total_lines": total_lines,
        "parse_errors": parse_errors,
        "total_dialogues": len(dialogues),
        "consistency_issues": consistency_issues
    }
    
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/audit_report.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"Audit completed successfully. Report saved to {output_path}")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
