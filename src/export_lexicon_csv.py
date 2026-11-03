import sys
import os
import traceback
import time
import json
import csv

def main():
    json_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/core_lexicon.json"
    csv_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/core_lexicon.csv"
    
    if not os.path.exists(json_path):
        print(f"Error: {json_path} does not exist.")
        sys.exit(1)
        
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}")
        traceback.print_exc()
        sys.exit(1)
        
    if isinstance(data, dict):
        lexicon_items = data.get("lexicon", [])
        if not lexicon_items:
            lexicon_items = [data]
    elif isinstance(data, list):
        lexicon_items = data
    else:
        print("Error: Unexpected JSON root structure.")
        sys.exit(1)
        
    try:
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = None
            for item in lexicon_items:
                if not isinstance(item, dict):
                    continue
                if writer is None:
                    fieldnames = list(item.keys())
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                writer.writerow(item)
        print(f"Successfully exported lexicon to {csv_path}")
    except Exception as e:
        print(f"Error writing CSV: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Fatal error: {e}")
        traceback.print_exc()
        sys.exit(1)
