import sys
import os
import traceback
import time
import json

def audit_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
        sys.exit(1)

    total_records = 0
    error_records = 0
    audit_results = []

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            total_records += 1
            try:
                record = json.loads(line)
                if "dialogue" not in record or not isinstance(record["dialogue"], list):
                    raise ValueError("Missing or invalid 'dialogue' field")
                
                prev_speaker = None
                for turn_idx, turn in enumerate(record["dialogue"]):
                    if "speaker" not in turn or "text" not in turn:
                        raise ValueError(f"Turn {turn_idx} missing speaker or text")
                    current_speaker = turn["speaker"]
                    if prev_speaker and current_speaker == prev_speaker:
                        print(f"Warning: Consecutive turns by same speaker '{current_speaker}' at record {line_num}, turn {turn_idx}")
                    prev_speaker = current_speaker
                
                audit_results.append({"id": record.get("id", line_num), "status": "OK"})
            except Exception as e:
                error_records += 1
                audit_results.append({"id": line_num, "status": "ERROR", "message": str(e)})
                print(f"Audit error at line {line_num}: {e}")

    report = {
        "total_records": total_records,
        "error_records": error_records,
        "results": audit_results
    }
    
    report_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/audit_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"Audit completed. Report saved to {report_path}")

if __name__ == "__main__":
    try:
        audit_res = audit_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
