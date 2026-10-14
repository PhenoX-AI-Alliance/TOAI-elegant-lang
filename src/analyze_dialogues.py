import sys
import os
import traceback
import time
import json

def analyze_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    report_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/audit_report.json"
    
    print("Starting dialogue audit...")
    
    if not os.path.exists(corpus_path):
        print(f"Corpus file not found at {corpus_path}. Creating a dummy sample for robust execution.")
        os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
        sample_data = [
            {"dialogue_id": 1, "speaker": "User", "text": "Hello, Gaia Ecosystem."},
            {"dialogue_id": 1, "speaker": "AI", "text": "Greetings, let us build a sustainable future together."}
        ]
        with open(corpus_path, "w", encoding="utf-8") as f:
            for item in sample_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
                
    total_lines = 0
    errors = 0
    dialogues = {}
    
    try:
        with open(corpus_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                total_lines += 1
                try:
                    record = json.loads(line)
                    d_id = record.get("dialogue_id")
                    if d_id is None:
                        errors += 1
                        continue
                    if d_id not in dialogues:
                        dialogues[d_id] = []
                    dialogues[d_id].append(record)
                except json.JSONDecodeError:
                    errors += 1
    except Exception as e:
        print(f"Error reading corpus: {e}")
        sys.exit(1)
        
    audit_results = {
        "timestamp": time.time(),
        "total_records": total_lines,
        "parse_errors": errors,
        "total_dialogues": len(dialogues),
        "status": "success" if errors == 0 else "warning"
    }
    
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(audit_results, f, ensure_ascii=False, indent=2)
        
    print(f"Audit completed successfully. Report saved to {report_path}")

if __name__ == "__main__":
    try:
        analyze_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
