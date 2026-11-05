# -*- coding: utf-8 -*-
import sys
import os
import json
import traceback

def audit_dialogues(corpus_path):
    issues = []
    total_dialogues = 0
    valid_dialogues = 0

    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {{corpus_path}}")
        sys.exit(1)

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            total_dialogues += 1
            try:
                data = json.loads(line)
            except json.JSONDecodeError as e:
                issues.append(f"Line {{line_num}}: Invalid JSON format - {{e}}")
                continue

            if "dialogue_id" not in data:
                issues.append(f"Line {{line_num}}: Missing 'dialogue_id'")
            
            turns = data.get("turns", [])
            if not isinstance(turns, list) or len(turns) == 0:
                issues.append(f"Line {{line_num}}: 'turns' field is missing or empty")
                continue

            expected_role = "user"
            dialogue_ok = True
            for turn_idx, turn in enumerate(turns):
                role = turn.get("role")
                content = turn.get("content")
                if role != expected_role:
                    issues.append(f"Line {{line_num}} turn {{turn_idx}}: Expected role '{{expected_role}}', got '{{role}}'")
                    dialogue_ok = False
                if not content or not isinstance(content, str):
                    issues.append(f"Line {{line_num}} turn {{turn_idx}}: Content is empty or not a string")
                    dialogue_ok = False
                expected_role = "assistant" if expected_role == "user" else "user"

            if dialogue_ok:
                valid_dialogues += 1

    print(f"Audit Complete.")
    print(f"Total Dialogues: {{total_dialogues}}")
    print(f"Valid Dialogues: {{valid_dialogues}}")
    print(f"Issues Found: {{len(issues)}}")
    
    for issue in issues:
        print(f" - {{issue}}")

    if issues:
        sys.exit(2)

if __name__ == "__main__":
    corpus = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    audit_dialogues(corpus)
