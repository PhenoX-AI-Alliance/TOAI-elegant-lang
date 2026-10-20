import sys
import os
import traceback
import time
import json
import csv

def convert_json_to_csv():
    base_dir = "/home/phenox/gemini-sandbox/TOAI_Generated"
    json_path = os.path.join(base_dir, "core_lexicon.json")
    csv_path = os.path.join(base_dir, "core_lexicon.csv")
    
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at {json_path}", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)
        
    lexicon_list = data.get("lexicon", [])
    if not lexicon_list:
        print("Warning: No lexicon entries found.", file=sys.stderr)
        
    try:
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "term", "category", "meaning"])
            for item in lexicon_list:
                writer.writerow([
                    item.get("id", ""),
                    item.get("term", ""),
                    item.get("category", ""),
                    item.get("meaning", "")
                ])
        print(f"Successfully exported lexicon to {csv_path}")
    except Exception as e:
        print(f"Error writing CSV: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    convert_json_to_csv()
