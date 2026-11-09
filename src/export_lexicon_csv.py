import sys
import os
import traceback
import time
import json
import csv

def main():
    try:
        base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        src_dir = os.path.join(base_dir, "src")
        data_dir = os.path.join(base_dir, "data")
        
        json_path = os.path.join(data_dir, "core_lexicon.json")
        csv_path = os.path.join(data_dir, "core_lexicon.csv")
        
        os.makedirs(data_dir, exist_ok=True)
        
        if not os.path.exists(json_path):
            sample_data = {
                "lexicon": [
                    {"id": 1, "term": "Gaia", "category": "ecosystem", "definition": "The living Earth system."},
                    {"id": 2, "term": "Altruism", "category": "philosophy", "definition": "Selfless concern for the well-being of others."}
                ]
            }
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(sample_data, f, ensure_ascii=False, indent=2)
        
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        items = data.get("lexicon", [])
        if not items and isinstance(data, list):
            items = data
            
        if not items:
            print("No lexicon items found in JSON.")
            sys.exit(0)
            
        keys = set()
        for item in items:
            if isinstance(item, dict):
                keys.update(item.keys())
                
        fieldnames = sorted(list(keys))
        
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in items:
                if isinstance(item, dict):
                    writer.writerow(item)
                    
        print(f"Successfully exported core_lexicon.json to {csv_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
