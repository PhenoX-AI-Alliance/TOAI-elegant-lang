import sys
import os
import traceback
import time
import json

def audit_dialogues(filepath):
    if not os.path.exists(filepath):
        print(f"Error: Corpus file not found at {{filepath}}")
        sys.exit(1)
        
    total_dialogues = 0
    errors = 0
    
    with open(filepath, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                total_dialogues += 1
                if "dialogue_id" not in data or "turns" not in data:
                    print(f"Line {{line_num}}: Missing required keys.")
                    errors += 1
                    continue
                turns = data["turns"]
                if not isinstance(turns, list) or len(turns) == 0:
                    print(f"Line {{line_num}}: Turns must be a non-empty list.")
                    errors += 1
                    continue
                expected_speaker = "user"
                for turn in turns:
                    if "speaker" not in turn or "text" not in turn:
                        print(f"Line {{line_num}}: Turn missing speaker or text.")
                        errors += 1
                        break
                    if turn["speaker"] != expected_speaker:
                        print(f"Line {{line_num}}: Speaker mismatch. Expected {{expected_speaker}}, got {{turn['speaker']}}")
                        errors += 1
                    expected_speaker = "assistant" if expected_speaker == "user" else "user"
            except json.JSONDecodeError as e:
                print(f"Line {{line_num}}: Invalid JSON -> {{e}}")
                errors += 1
                
    print(f"Audit Complete. Total Dialogues: {{total_dialogues}}, Errors Found: {{errors}}")
    if errors > 0:
        sys.exit(1)

if __name__ == "__main__":
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    audit_dialogues(corpus_path)
