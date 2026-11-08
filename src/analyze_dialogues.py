import sys
import os
import traceback
import json

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    print(f"Loading corpus from {{corpus_path}}...")
    
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {{corpus_path}}")
        sys.exit(1)

    total_lines = 0
    valid_dialogues = 0
    errors = []

    with open(corpus_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, 1):
            total_lines += 1
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if not isinstance(data, dict):
                    errors.append((idx, "Root element is not a dictionary"))
                    continue
                
                if "dialogue" not in data and "messages" not in data:
                    errors.append((idx, "Missing dialogue or messages key"))
                    continue
                
                valid_dialogues += 1
            except json.JSONDecodeError as e:
                errors.append((idx, f"JSON Decode Error: {{e}}"))

    print(f"Total lines read: {{total_lines}}")
    print(f"Valid dialogues: {{valid_dialogues}}")
    print(f"Audit errors found: {{len(errors)}}")

    if errors:
        print("Detailed errors:")
        for line_num, err in errors[:10]:
            print(f"  Line {{line_num}}: {{err}}")
        if len(errors) > 10:
            print(f"  ... and {{len(errors) - 10}} more errors.")

    report = {
        "total_lines": total_lines,
        "valid_dialogues": valid_dialogues,
        "error_count": len(errors),
        "errors": errors[:50]
    }

    report_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/audit_report.json"
    with open(report_path, "w", encoding="utf-8") as rf:
        json.dump(report, rf, ensure_ascii=False, indent=2)
    print(f"Audit report saved to {{report_path}}")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
