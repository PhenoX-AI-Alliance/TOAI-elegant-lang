import sys
import os
import traceback
import time
import json

def audit_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        raise FileNotFoundError(f"Corpus file not found: {corpus_path}")
        
    dialogues = {}
    total_lines = 0
    parse_errors = 0
    
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            total_lines += 1
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                did = record.get("dialogue_id")
                if did is None:
                    parse_errors += 1
                    continue
                if did not in dialogues:
                    dialogues[did] = []
                dialogues[did].append(record)
            except json.JSONDecodeError:
                parse_errors += 1
                
    audit_results = {
        "total_lines": total_lines,
        "parse_errors": parse_errors,
        "total_dialogues": len(dialogues),
        "malformed_dialogues": 0
    }
    
    for did, turns in dialogues.items():
        expected_speaker = "user"
        for idx, turn in enumerate(turns):
            speaker = turn.get("speaker")
            if idx % 2 == 0:
                if speaker != "user":
                    audit_results["malformed_dialogues"] += 1
                    break
            else:
                if speaker != "assistant":
                    audit_results["malformed_dialogues"] += 1
                    break
                    
    print(json.dumps(audit_results, indent=2))

if __name__ == "__main__":
    try:
        audit_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
