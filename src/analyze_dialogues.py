import sys
import os
import traceback
import time
import json

def audit_dialogues(corpus_path, report_path):
    total_dialogues = 0
    valid_dialogues = 0
    errors = []

    if not os.path.exists(corpus_path):
        raise FileNotFoundError(f"Corpus not found: {corpus_path}")

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            total_dialogues += 1
            try:
                data = json.loads(line)
                if "turns" not in data or not isinstance(data["turns"], list):
                    errors.append(f"Line {line_num}: Missing 'turns' list.")
                    continue
                
                turns = data["turns"]
                if len(turns) == 0:
                    errors.append(f"Line {line_num}: Empty turns.")
                    continue

                last_role = None
                turn_error = False
                for t_idx, turn in enumerate(turns):
                    if "role" not in turn or "text" not in turn:
                        errors.append(f"Line {line_num}, Turn {t_idx}: Missing role or text.")
                        turn_error = True
                        break
                    current_role = turn["role"]
                    if current_role == last_role:
                        errors.append(f"Line {line_num}, Turn {t_idx}: Consecutive same role ({current_role}).")
                        turn_error = True
                        break
                    last_role = current_role

                if not turn_error:
                    valid_dialogues += 1

            except json.JSONDecodeError as jde:
                errors.append(f"Line {line_num}: Invalid JSON - {jde}")

    report = {
        "total_dialogues": total_dialogues,
        "valid_dialogues": valid_dialogues,
        "error_count": len(errors),
        "errors": errors
    }

    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as rf:
        json.dump(report, rf, ensure_ascii=False, indent=2)

    print(f"Audit completed. Total: {total_dialogues}, Valid: {valid_dialogues}, Errors: {len(errors)}")

if __name__ == "__main__":
    corpus = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    report = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/audit_report.json"
    audit_dialogues(corpus, report)
