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
        output_dir = os.path.join(base_dir, "output")
        
        os.makedirs(output_dir, exist_ok=True)
        
        json_path = os.path.join(data_dir, "core_lexicon.json")
        csv_path = os.path.join(output_dir, "core_lexicon_export.csv")
        
        if not os.path.exists(json_path):
            os.makedirs(data_dir, exist_ok=True)
            default_data = [
                {"id": 1, "term": "Gaia", "category": "ecosystem", "description": "The living Earth ecosystem."},
                {"id": 2, "term": "Altruism", "category": "philosophy", "description": "Selfless concern for the well-being of others."}
            ]
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(default_data, f, ensure_ascii=False, indent=2)
                
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        if not isinstance(data, list):
            if isinstance(data, dict):
                data = [data]
            else:
                data = [{"content": str(data)}]
                
        fieldnames = set()
        for item in data:
            if isinstance(item, dict):
                fieldnames.update(item.keys())
                
        if not fieldnames:
            fieldnames = ["term", "definition"]
            
        fieldnames = sorted(list(fieldnames))
        
        with open(csv_path, "w", encoding="utf-8", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item in data:
                if isinstance(item, dict):
                    row = {k: str(item.get(k, "")) for k in fieldnames}
                    writer.writerow(row)
                else:
                    writer.writerow({fieldnames[0]: str(item)})
                    
        print(f"Successfully exported lexicon to {csv_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
