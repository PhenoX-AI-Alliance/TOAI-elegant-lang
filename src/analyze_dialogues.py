import sys
import os
import traceback
import json

def analyze_corpus():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/dialogue_audit_report.json"
    
    print(f"Starting dialogue audit from: {corpus_path}")
    
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
        report = {
            "status": "error",
            "message": "corpus/dialogues.jsonl not found",
            "total_lines": 0,
            "valid_dialogues": 0,
            "errors": []
        }
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        return

    total_lines = 0
    valid_dialogues = 0
    errors = []

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            total_lines += 1
            line_str = line.strip()
            if not line_str:
                continue
            try:
                data = json.loads(line_str)
                if not isinstance(data, dict):
                    errors.append({"line": line_num, "error": "JSON root is not an object"})
                    continue
                
                if "messages" not in data and "dialogue" not in data:
                    errors.append({"line": line_num, "error": "Missing 'messages' or 'dialogue' key"})
                    continue
                
                valid_dialogues += 1
            except json.JSONDecodeError as jde:
                errors.append({"line": line_num, "error": f"JSONDecodeError: {str(jde)}"})
            except Exception as ex:
                errors.append({"line": line_num, "error": str(ex)})

    report = {
        "status": "success",
        "total_lines": total_lines,
        "valid_dialogues": valid_dialogues,
        "error_count": len(errors),
        "errors": errors
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        
    print(f"Dialogue audit completed successfully. Report saved to {output_path}")

if __name__ == "__main__":
    try:
        analyze_corpus()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
