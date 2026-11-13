import sys
import os
import traceback
import time
import json

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/analysis_report.json"
    
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
        sys.exit(1)
        
    total_lines = 0
    valid_dialogues = 0
    errors = []
    
    with open(corpus_path, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f, 1):
            total_lines += 1
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if not isinstance(data, dict):
                    errors.append({"line": idx, "error": "Not a JSON object"})
                    continue
                if "messages" not in data or not isinstance(data["messages"], list):
                    errors.append({"line": idx, "error": "Missing 'messages' list"})
                    continue
                
                messages = data["messages"]
                if len(messages) == 0:
                    errors.append({"line": idx, "error": "Empty messages list"})
                    continue
                
                role_sequence_valid = True
                for m_idx, msg in enumerate(messages):
                    if not isinstance(msg, dict) or "role" not in msg or "content" not in msg:
                        role_sequence_valid = False
                        break
                
                if role_sequence_valid:
                    valid_dialogues += 1
                else:
                    errors.append({"line": idx, "error": "Invalid message structure"})
                    
            except json.JSONDecodeError as e:
                errors.append({"line": idx, "error": f"JSONDecodeError: {str(e)}"})
                
    report = {
        "timestamp": time.time(),
        "total_lines": total_lines,
        "valid_dialogues": valid_dialogues,
        "error_count": len(errors),
        "errors": errors
    }
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as out_f:
        json.dump(report, out_f, ensure_ascii=False, indent=2)
        
    print(f"Analysis complete. Valid dialogues: {valid_dialogues}/{total_lines}. Report saved to {output_path}")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
