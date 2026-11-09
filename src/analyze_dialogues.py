import sys
import os
import traceback
import json

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
        sys.exit(1)

    total_dialogues = 0
    malformed_count = 0
    audit_results = []

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                total_dialogues += 1
                if "dialogue_id" not in data or "turns" not in data:
                    malformed_count += 1
                    audit_results.append({"line": line_num, "error": "Missing required keys"})
                    continue
                turns = data["turns"]
                if not isinstance(turns, list) or len(turns) == 0:
                    malformed_count += 1
                    audit_results.append({"line": line_num, "error": "Turns is empty or not a list"})
                    continue
                
                expected_role = "user"
                role_error = False
                for turn in turns:
                    if "role" not in turn or "content" not in turn:
                        role_error = True
                        break
                    if turn["role"] != expected_role:
                        role_error = True
                        break
                    expected_role = "assistant" if expected_role == "user" else "user"
                
                if role_error:
                    malformed_count += 1
                    audit_results.append({"line": line_num, "error": "Turn alternation role mismatch or missing fields"})
            except json.JSONDecodeError:
                malformed_count += 1
                audit_results.append({"line": line_num, "error": "Invalid JSON format"})

    report = {
        "total_dialogues": total_dialogues,
        "malformed_count": malformed_count,
        "audit_results": audit_results
    }
    
    report_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/audit_report.json"
    with open(report_path, "w", encoding="utf-8") as rf:
        json.dump(report, rf, ensure_ascii=False, indent=2)
    
    print(f"Audit completed. Total: {total_dialogues}, Malformed: {malformed_count}")
    print(f"Report saved to {report_path}")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
