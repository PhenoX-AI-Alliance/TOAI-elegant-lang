import sys
import os
import traceback
import json
import csv

def convert_lexicon():
    script_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src"
    json_path = os.path.join(script_dir, "core_lexicon.json")
    csv_path = os.path.join(script_dir, "core_lexicon.csv")
    
    if not os.path.exists(json_path):
        print(f"Error: {json_path} does not exist.", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}", file=sys.stderr)
        sys.exit(1)
        
    lexicon_items = data.get("lexicon", [])
    if not lexicon_items:
        print("Warning: No lexicon items found in JSON.", file=sys.stderr)
        
    try:
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["term", "category", "description"])
            for item in lexicon_items:
                writer.writerow([
                    item.get("term", ""),
                    item.get("category", ""),
                    item.get("description", "")
                ])
        print(f"Successfully exported lexicon to {csv_path}")
    except Exception as e:
        print(f"Error writing CSV: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    try:
        convert_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
