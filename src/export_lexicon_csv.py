import sys
import os
import json
import csv

def export_lexicon():
    json_path = "core_lexicon.json"
    csv_path = "core_lexicon.csv"
    
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        sys.exit(1)
        
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    if isinstance(data, dict):
        lexicon_list = data.get("lexicon", [])
    elif isinstance(data, list):
        lexicon_list = data
    else:
        lexicon_list = []
        
    fieldnames = ["id", "term", "definition"]
    if lexicon_list and isinstance(lexicon_list[0], dict):
        fieldnames = list(lexicon_list[0].keys())
        
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in lexicon_list:
            if isinstance(item, dict):
                writer.writerow(item)
                
    print(f"Successfully exported {len(lexicon_list)} items to {csv_path}")

if __name__ == "__main__":
    export_lexicon()
