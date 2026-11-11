import sys
import os
import json
import csv

def export_csv():
    target_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src"
    json_path = os.path.join(target_dir, "core_lexicon.json")
    csv_path = os.path.join(target_dir, "export_lexicon.csv")
    
    if not os.path.exists(json_path):
        print(f"Error: {json_path} does not exist.")
        sys.exit(1)
        
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    if not isinstance(data, list) or len(data) == 0:
        raise ValueError("JSON data must be a non-empty list of dictionaries.")
        
    keys = set()
    for item in data:
        if isinstance(item, dict):
            keys.update(item.keys())
            
    fieldnames = sorted(list(keys))
    
    with open(csv_path, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            if isinstance(item, dict):
                writer.writerow(item)
    print(f"Successfully exported to {csv_path}")

if __name__ == "__main__":
    export_csv()
