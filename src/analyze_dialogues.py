import sys
import os
import traceback
import time
import json

def audit_dialogues(corpus_file):
    total_dialogues = 0
    valid_dialogues = 0
    error_turns = 0
    anomalies = []

    if not os.path.exists(corpus_file):
        print(f"Error: Corpus file not found at {corpus_file}")
        sys.exit(1)

    with open(corpus_file, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            total_dialogues += 1
            try:
                data = json.loads(line)
            except json.JSONDecodeError as e:
                anomalies.append({"line": line_num, "error": f"JSONDecodeError: {str(e)}"})
                continue

            if "dialogue_id" not in data or "turns" not in data:
                anomalies.append({"line": line_num, "error": "Missing dialogue_id or turns"})
                continue

            turns = data["turns"]
            if not isinstance(turns, list) or len(turns) == 0:
                anomalies.append({"line": line_num, "error": "Turns is empty or not a list"})
                continue

            dialogue_valid = True
            for turn in turns:
                if "role" not in turn or "content" not in turn:
                    dialogue_valid = False
                    anomalies.append({"line": line_num, "error": "Turn missing role or content"})
                    break
                if turn["role"] == "error":
                    error_turns += 1

            if dialogue_valid:
                valid_dialogues += 1

    report = {
        "timestamp": time.time(),
        "total_dialogues": total_dialogues,
        "valid_dialogues": valid_dialogues,
        "error_turns": error_turns,
        "anomalies": anomalies
    }

    report_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/audit_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"Audit completed. Total: {total_dialogues}, Valid: {valid_dialogues}, Errors: {error_turns}")
    print(f"Report saved to {report_path}")

if __name__ == "__main__":
    corpus_file = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    audit_dialogues(corpus_file)
