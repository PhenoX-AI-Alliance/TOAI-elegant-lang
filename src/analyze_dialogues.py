import sys
import os
import traceback
import time
import json

def analyze_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {corpus_path}")
        sys.exit(1)

    total_lines = 0
    valid_dialogues = 0
    errors = []

    with open(corpus_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, 1):
            total_lines += 1
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if not isinstance(data, dict):
                    raise ValueError("Root element must be an object")
                if "messages" not in data or not isinstance(data["messages"], list):
                    raise ValueError("Missing 'messages' list")
                
                messages = data["messages"]
                if len(messages) == 0:
                    raise ValueError("Messages list is empty")

                for m_idx, msg in enumerate(messages):
                    if not isinstance(msg, dict):
                        raise ValueError(f"Message at index {m_idx} is not an object")
                    if "role" not in msg or "content" not in msg:
                        raise ValueError(f"Message at index {m_idx} missing 'role' or 'content'")

                valid_dialogues += 1
            except Exception as e:
                errors.append({"line": idx, "error": str(e)})

    report = {
        "total_lines": total_lines,
        "valid_dialogues": valid_dialogues,
        "error_count": len(errors),
        "errors": errors
    }

    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    try:
        analyze_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
