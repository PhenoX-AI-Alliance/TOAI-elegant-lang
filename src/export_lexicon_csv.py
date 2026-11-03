import sys
import os
import json
import csv

def export_csv():
    target_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src"
    json_path = os.path.join(target_dir, "core_lexicon.json")
    csv_path = os.path.join(target_dir, "core_lexicon.csv")
    
    if not os.path.exists(json_path):
        print("Error: core_lexicon.json not found.")
        sys.exit(1)
        
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    if isinstance(data, dict):
        items = data.get("lexicon", [])
    elif isinstance(data, list):
        items = data
    else:
        items = []
        
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["term", "category", "description"])
        for item in items:
            if isinstance(item, dict):
                writer.writerow([
                    item.get("term", ""),
                    item.get("category", ""),
                    item.get("description", "")
                ])
    print("Successfully exported core_lexicon.csv")

if __name__ == "__main__":
    export_csv()
