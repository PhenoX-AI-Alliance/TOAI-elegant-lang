import sys
import os
import json
import csv

def convert():
    json_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/core_lexicon.json"
    csv_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/export_lexicon.csv"
    
    if not os.path.exists(json_path):
        json_path = "/home/phenox/gemini-sandbox/TOAI_Generated/core_lexicon.json"
        csv_path = "/home/phenox/gemini-sandbox/TOAI_Generated/export_lexicon.csv"
        
    if not os.path.exists(json_path):
        print(f"Source JSON not found: {json_path}")
        sys.exit(1)
        
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    items = []
    if isinstance(data, dict):
        if "lexicon" in data and isinstance(data["lexicon"], list):
            items = data["lexicon"]
        else:
            items = [data]
    elif isinstance(data, list):
        items = data
        
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    
    fieldnames = set()
    for item in items:
        if isinstance(item, dict):
            fieldnames.update(item.keys())
            
    fieldnames_list = sorted(list(fieldnames))
    if not fieldnames_list:
        fieldnames_list = ["id", "term", "category", "description"]
        
    with open(csv_path, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames_list)
        writer.writeheader()
        for item in items:
            if isinstance(item, dict):
                writer.writerow(item)
                
    print(f"Successfully exported {len(items)} items to {csv_path}")

if __name__ == "__main__":
    try:
        convert()
    except Exception as e:
        print(f"Error during export: {e}", file=sys.stderr)
        sys.exit(1)
