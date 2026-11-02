# -*- coding: utf-8 -*-
import sys
import os
import json
import csv
import traceback

def export_csv():
    source_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/core_lexicon.json"
    dest_path = "/home/phenox/gemini-sandbox/TOAI_Generated/core_lexicon.csv"
    
    if not os.path.exists(source_path):
        print(f"Error: Source JSON file not found at {source_path}")
        sys.exit(1)
        
    try:
        with open(source_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        
        with open(dest_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["key", "value", "description"])
            
            if isinstance(data, dict):
                for k, v in data.items():
                    if isinstance(v, dict):
                        val_str = v.get("value", str(v))
                        desc_str = v.get("description", "")
                        writer.writerow([k, val_str, desc_str])
                    else:
                        writer.writerow([k, str(v), ""])
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        k = item.get("key", "")
                        v = item.get("value", "")
                        d = item.get("description", "")
                        writer.writerow([k, v, d])
                    else:
                        writer.writerow(["", str(item), ""])
                        
        print(f"Successfully exported lexicon to {dest_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    export_csv()
