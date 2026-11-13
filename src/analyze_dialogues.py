import sys
import os
import traceback
import time
import json

def analyze_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/audit_report.json"
    
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
        sys.exit(1)
        
    total_lines = 0
    valid_dialogues = 0
    errors = []
    
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            total_lines += 1
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if not isinstance(data, dict):
                    errors.append({"line": line_num, "error": "Root element is not a JSON object"})
                    continue
                
                if "messages" not in data or not isinstance(data["messages"], list):
                    errors.append({"line": line_num, "error": "Missing or invalid 'messages' field"})
                    continue
                
                messages = data["messages"]
                if len(messages) == 0:
                    errors.append({"line": line_num, "error": "Empty messages list"})
                    continue
                
                # Check role alternation consistency
                consistent = True
                expected_role = "user"
                for msg in messages:
                    if not isinstance(msg, dict) or "role" not in msg or "content" not in msg:
                        consistent = False
                        break
                
                if not consistent:
                    errors.append({"line": line_num, "error": "Invalid message structure"})
                    continue
                
                valid_dialogues += 1
            except json.JSONDecodeError as jde:
                errors.append({"line": line_num, "error": f"JSON decode error: {str(jde)}"})
            except Exception as e:
                errors.append({"line": line_num, "error": f"Unexpected error: {str(e)}"})
                
    report = {
        "timestamp": time.time(),
        "total_lines": total_lines,
        "valid_dialogues": valid_dialogues,
        "error_count": len(errors),
        "errors": errors
    }
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(report, out, ensure_ascii=False, indent=2)
        
    print(f"Analysis complete. Valid: {valid_dialogues}, Errors: {len(errors)}")
    print(f"Report saved to {output_path}")

if __name__ == "__main__":
    try:
        analyze_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
