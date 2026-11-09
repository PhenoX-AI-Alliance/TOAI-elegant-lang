import sys
import os
import traceback
import time
import json

def audit_dialogues(file_path):
    issues = []
    total = 0
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Corpus file not found at {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            total += 1
            try:
                data = json.loads(line)
            except json.JSONDecodeError as e:
                issues.append({"line": line_num, "error": f"JSONDecodeError: {str(e)}"})
                continue
            
            if "turns" not in data:
                issues.append({"line": line_num, "error": "Missing 'turns' key"})
                continue
            
            turns = data["turns"]
            if not isinstance(turns, list) or len(turns) == 0:
                issues.append({"line": line_num, "error": "'turns' must be a non-empty list"})
                continue
            
            expected_speaker = "user"
            for turn_idx, turn in enumerate(turns):
                if not isinstance(turn, dict):
                    issues.append({"line": line_num, "error": f"Turn {turn_idx} is not a dict"})
                    break
                if "speaker" not in turn or "text" not in turn:
                    issues.append({"line": line_num, "error": f"Turn {turn_idx} missing 'speaker' or 'text'"})
                    break
                
                current_speaker = turn["speaker"]
                if current_speaker != expected_speaker:
                    issues.append({"line": line_num, "warning": f"Speaker sequence anomaly at turn {turn_idx}: expected {expected_speaker}, got {current_speaker}"})
                
                expected_speaker = "assistant" if current_speaker == "user" else "user"
                
    return {"total_dialogues": total, "issues": issues}

def main():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    print(f"Auditing corpus at: {corpus_path}")
    result = audit_dialogues(corpus_path)
    print(f"Audit completed. Total dialogues: {result['total_dialogues']}")
    print(f"Total issues found: {len(result['issues'])}")
    for issue in result["issues"]:
        print(json.dumps(issue, ensure_ascii=False))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
