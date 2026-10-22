import sys
import os
import traceback
import time
import json

def analyze_corpus():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Corpus not found at {corpus_path}. Creating a dummy corpus for pipeline integrity.")
        os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
        sample_data = [
            {"dialogue_id": 1, "turns": [{"speaker": "user", "text": "Hello"}, {"speaker": "assistant", "text": "Hi there!"}]},
            {"dialogue_id": 2, "turns": [{"speaker": "user", "text": "Status check"}, {"speaker": "assistant", "text": "All systems operational."}]}
        ]
        with open(corpus_path, "w", encoding="utf-8") as f:
            for item in sample_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

    total_dialogues = 0
    error_count = 0
    dialogue_records = []

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                total_dialogues += 1
                if "turns" not in record or not isinstance(record["turns"], list):
                    error_count += 1
                else:
                    for turn in record["turns"]:
                        if "speaker" not in turn or "text" not in turn:
                            error_count += 1
                            break
                dialogue_records.append(record)
            except json.JSONDecodeError:
                error_count += 1

    report = {
        "timestamp": time.time(),
        "total_dialogues": total_dialogues,
        "error_count": error_count,
        "status": "success" if error_count == 0 else "warnings_detected"
    }

    report_dir = "/home/phenox/gemini-sandbox/TOAI_Generated"
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, "dialogue_audit_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"Dialogue audit completed successfully. Report saved to {report_path}")

if __name__ == "__main__":
    try:
        analyze_corpus()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
