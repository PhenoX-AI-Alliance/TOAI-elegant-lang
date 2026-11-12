import sys
import os
import traceback
import time
import json
import csv

def export_lexicon():
    try:
        base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src"
        json_path = os.path.join(base_dir, "core_lexicon.json")
        csv_path = os.path.join(base_dir, "core_lexicon.csv")
        
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"core_lexicon.json not found at {json_path}")
            
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        if isinstance(data, dict):
            data = [data]
        elif not isinstance(data, list):
            raise ValueError("JSON data must be a list or dictionary.")
            
        if len(data) == 0:
            raise ValueError("JSON data must be a non-empty list of dictionaries.")
            
        fieldnames = set()
        for item in data:
            if isinstance(item, dict):
                fieldnames.update(item.keys())
            else:
                raise ValueError("JSON elements must be dictionaries.")
                
        fieldnames_list = sorted(list(fieldnames))
        
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames_list)
            writer.writeheader()
            for item in data:
                writer.writerow(item)
                
        print(f"Successfully exported {len(data)} items to {csv_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    export_lexicon()
