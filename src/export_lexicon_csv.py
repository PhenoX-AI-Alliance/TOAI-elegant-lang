import sys
import os
import json
import csv

def export_lexicon():
    base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
    json_path = os.path.join(base_dir, "core_lexicon.json")
    csv_path = os.path.join(base_dir, "src", "lexicon_export.csv")
    
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        sys.exit(1)
        
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    items = []
    if isinstance(data, dict):
        if "items" in data and isinstance(data["items"], list):
            items = data["items"]
        elif "lexicon" in data and isinstance(data["lexicon"], list):
            items = data["lexicon"]
        else:
            for k, v in data.items():
                if isinstance(v, dict):
                    v["key"] = k
                    items.append(v)
                else:
                    items.append({"key": k, "value": str(v)})
    elif isinstance(data, list):
        items = data
        
    if not items:
        print("Error: No lexicon items found.")
        sys.exit(1)
        
    fieldnames = set()
    for item in items:
        if isinstance(item, dict):
            fieldnames.update(item.keys())
    fieldnames = sorted(list(fieldnames))
    
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in items:
            if isinstance(item, dict):
                row = {k: item.get(k, "") for k in fieldnames}
                writer.writerow(row)
                
    print(f"Successfully exported {len(items)} items to {csv_path}")

if __name__ == "__main__":
    export_lexicon()
