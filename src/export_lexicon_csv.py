# -*- coding: utf-8 -*-
import sys
import os
import traceback
import time
import json
import csv

def export_csv():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, "core_lexicon.json")
    csv_path = os.path.join(base_dir, "core_lexicon.csv")
    
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
        
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        entries = data.get("entries", [])
        
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["term", "category", "meaning"])
            for entry in entries:
                writer.writerow([
                    entry.get("term", ""),
                    entry.get("category", ""),
                    entry.get("meaning", "")
                ])
                
        print(f"Successfully exported lexicon to {csv_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    export_csv()
