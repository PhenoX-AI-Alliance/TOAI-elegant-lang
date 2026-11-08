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
        
    total_lines = 0
    errors = 0
    dialogue_map = {}
    
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            total_lines += 1
            try:
                record = json.loads(line)
                d_id = record.get("dialogue_id")
                speaker = record.get("speaker")
                text = record.get("text")
                
                if d_id is None or speaker is None or text is None:
                    print(f"Line {line_num}: Missing required fields.")
                    errors += 1
                    continue
                    
                if d_id not in dialogue_map:
                    dialogue_map[d_id] = []
                dialogue_map[d_id].append({"speaker": speaker, "text": text})
            except json.JSONDecodeError as e:
                print(f"Line {line_num}: Invalid JSON format - {e}")
                errors += 1
                
    for d_id, turns in dialogue_map.items():
        if len(turns) < 2:
            print(f"Dialogue {d_id}: Incomplete exchange (less than 2 turns).")
            errors += 1
            
    print(f"Audit completed. Total lines: {total_lines}, Dialogues evaluated: {len(dialogue_map)}, Errors found: {errors}")
    if errors > 0:
        sys.exit(1)

if __name__ == "__main__":
    try:
        audit_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
