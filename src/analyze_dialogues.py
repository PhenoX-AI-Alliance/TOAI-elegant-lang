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

    try:
        with open(corpus_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                total_lines += 1
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    if not isinstance(data, dict):
                        errors.append(f"Line {line_num}: Not a JSON object")
                        continue
                    
                    if "dialogue" not in data and "messages" not in data:
                        errors.append(f"Line {line_num}: Missing dialogue or messages key")
                        continue
                    
                    valid_dialogues += 1
                except json.JSONDecodeError as jde:
                    errors.append(f"Line {line_num}: JSON decode error: {jde}")
                except Exception as e:
                    errors.append(f"Line {line_num}: Unexpected error: {e}")

        report = {
            "timestamp": time.time(),
            "total_lines": total_lines,
            "valid_dialogues": valid_dialogues,
            "error_count": len(errors),
            "errors": errors[:50]
        }

        report_path = "/home/phenox/gemini-sandbox/TOAI_Generated/dialogue_audit_report.json"
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as rf:
            json.dump(report, rf, ensure_ascii=False, indent=2)

        print(f"Audit completed successfully. Valid: {valid_dialogues}/{total_lines}. Report saved to {report_path}")

    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    audit_dialogues()
