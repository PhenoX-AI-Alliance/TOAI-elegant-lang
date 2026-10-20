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
        print(f"Failed to parse JSON: {e}")
        traceback.print_exc()
        sys.exit(1)
        
    try:
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["key", "value", "description"])
            if isinstance(data, dict):
                for k, v in data.items():
                    if isinstance(v, dict):
                        writer.writerow([k, v.get("value", ""), v.get("description", "")])
                    else:
                        writer.writerow([k, str(v), ""])
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        writer.writerow([
                            item.get("key", ""),
                            item.get("value", ""),
                            item.get("description", "")
                        ])
                    else:
                        writer.writerow(["", str(item), ""])
        print(f"Successfully exported lexicon to {csv_path}")
    except Exception as e:
        print(f"Failed to write CSV: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Unhandled exception: {e}")
        traceback.print_exc()
        sys.exit(1)
