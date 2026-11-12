import sys
import os
import traceback
import time
import json

def audit_dialogues(corpus_file):
    results = {
        "total_dialogues": 0,
        "valid_dialogues": 0,
        "errors": []
    }
    
    if not os.path.exists(corpus_file):
        raise FileNotFoundError(f"Corpus file not found: {corpus_file}")

    with open(corpus_file, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            results["total_dialogues"] += 1
            try:
                data = json.loads(line)
                if "dialogue_id" not in data:
                    raise ValueError(f"Missing dialogue_id at line {line_num}")
                if "turns" not in data or not isinstance(data["turns"], list):
                    raise ValueError(f"Missing or invalid turns at line {line_num}")
                
                turns = data["turns"]
                if len(turns) == 0:
                    raise ValueError(f"Empty turns list at line {line_num}")
                
                prev_role = None
                for turn_idx, turn in enumerate(turns):
                    if "role" not in turn or "content" not in turn:
                        raise ValueError(f"Turn {turn_idx} missing role or content at line {line_num}")
                    role = turn["role"]
                    if role not in ["user", "assistant", "system"]:
                        raise ValueError(f"Invalid role '{role}' at line {line_num}")
                    prev_role = role
                
                results["valid_dialogues"] += 1
            except Exception as e:
                results["errors"].append({"line": line_num, "error": str(e)})

    return results

def main():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    report_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/audit_report.json"
    
    print(f"Starting dialogue analysis for: {corpus_path}")
    audit_results = audit_dialogues(corpus_path)
    
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(audit_results, f, ensure_ascii=False, indent=2)
        
    print(f"Audit completed. Report saved to {report_path}")
    print(json.dumps(audit_results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
