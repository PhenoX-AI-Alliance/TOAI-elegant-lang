import sys
import os
import traceback
import time
import json
import csv

def export_lexicon():
    try:
        base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        json_path = os.path.join(base_dir, "core_lexicon.json")
        csv_path = os.path.join(base_dir, "core_lexicon.csv")
        
        if not os.path.exists(json_path):
            print(f"Error: {json_path} does not exist.")
            sys.exit(1)
            
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        lexicon_items = data.get("lexicon", [])
        
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["term", "category", "description"])
            for item in lexicon_items:
                writer.writerow([
                    item.get("term", ""),
                    item.get("category", ""),
                    item.get("description", "")
                ])
                
        print(f"Successfully exported lexicon to {csv_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    export_lexicon()
