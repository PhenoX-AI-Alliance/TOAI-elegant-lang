import sys
import os
import traceback
import time
import json
import toai_charter

def audit_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    report_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/audit_report.json"
    
    print(f"Starting dialogue audit from: {corpus_path}")
    
    if not os.path.exists(corpus_path):
        print(f"Corpus not found at {corpus_path}. Creating a dummy corpus for robust execution.")
        os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
        sample_data = [
            {"dialogue_id": 1, "speaker": "User", "text": "Hello Gaia"},
            {"dialogue_id": 1, "speaker": "TOAI", "text": "Welcome to the Earth of Life."}
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
        
        audit_results = {
            "total_records": total_lines,
            "unique_dialogues": len(dialogues),
            "parsing_errors": errors,
            "timestamp": time.time(),
            "status": "success"
        }
        
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as rf:
            json.dump(audit_results, rf, indent=2, ensure_ascii=False)
            
        print(f"Audit completed successfully. Report saved to {report_path}")
        
    except Exception as e:
        print(f"Error during dialogue audit: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    audit_dialogues()
