import sys
import os
import traceback
import time
import json

def analyze_corpus(file_path):
    print(f"Starting analysis of corpus: {file_path}")
    if not os.path.exists(file_path):
        print(f"Error: Corpus file not found at {file_path}")
        sys.exit(1)
        
    total_dialogues = 0
    errors = 0
    
    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                total_dialogues += 1
                if "dialogue_id" not in data or "turns" not in data:
                    print(f"Warning: Line {line_num} missing required keys.")
                    errors += 1
                else:
                    turns = data["turns"]
                    if not isinstance(turns, list) or len(turns) == 0:
                        print(f"Warning: Dialogue {data.get('dialogue_id')} has invalid or empty turns.")
                        errors += 1
            except json.JSONDecodeError as e:
                print(f"JSONDecodeError at line {line_num}: {e}")
                errors += 1
                
    print(f"Analysis complete. Total dialogues: {total_dialogues}, Errors found: {errors}")
    return {"total": total_dialogues, "errors": errors}

if __name__ == "__main__":
    try:
        corpus_file = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
        result = analyze_corpus(corpus_file)
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
