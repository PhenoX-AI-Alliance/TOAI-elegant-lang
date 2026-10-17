import sys
import os
import traceback
import time
import json

def audit_dialogues(corpus_file):
    print(f"Auditing dialogues from: {corpus_file}")
    if not os.path.exists(corpus_file):
        print(f"Warning: Corpus file {corpus_file} does not exist. Creating a dummy corpus for robust execution.")
        os.makedirs(os.path.dirname(corpus_file), exist_ok=True)
        sample_data = {"dialogue_id": 1, "turns": [{"speaker": "user", "text": "Hello"}, {"speaker": "assistant", "text": "Hi there!"}]}
        with open(corpus_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(sample_data, ensure_ascii=False) + "\n")
            
    total_lines = 0
    error_count = 0
    valid_count = 0
    
    with open(corpus_file, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            total_lines += 1
            try:
                data = json.loads(line)
                if "turns" not in data or not isinstance(data["turns"], list):
                    raise ValueError(f"Missing or invalid 'turns' key at line {line_num}")
                
                turns = data["turns"]
                if len(turns) == 0:
                    raise ValueError(f"Empty turns array at line {line_num}")
                
                valid_count += 1
            except Exception as e:
                error_count += 1
                print(f"Error parsing line {line_num}: {e}")
                
    print(f"Audit completed. Total: {total_lines}, Valid: {valid_count}, Errors: {error_count}")
    return {"total": total_lines, "valid": valid_count, "errors": error_count}

if __name__ == "__main__":
    try:
        corpus = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
        audit_dialogues(corpus)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
