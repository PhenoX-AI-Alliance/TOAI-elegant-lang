import sys
import os
import traceback
import time
import json
import csv

def export_lexicon():
    try:
        sandbox_dir = "/home/phenox/gemini-sandbox"
        json_path = os.path.join(sandbox_dir, "TOAI-elegant-lang", "src", "core_lexicon.json")
        csv_path = os.path.join(sandbox_dir, "TOAI-elegant-lang", "src", "core_lexicon.csv")
        
        if not os.path.exists(json_path):
            print(f"Error: {json_path} does not exist.")
            sys.exit(1)
            
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        if isinstance(data, dict):
            rows = []
            for k, v in data.items():
                if isinstance(v, dict):
                    row = {"key": k}
                    row.update(v)
                    rows.append(row)
                else:
                    rows.append({"key": k, "value": v})
        elif isinstance(data, list):
            rows = data
        else:
            print("Error: Unsupported JSON format for CSV conversion.")
            sys.exit(1)
            
        if not rows:
            print("Error: No data to export.")
            sys.exit(1)
            
        fieldnames = set()
        for row in rows:
            if isinstance(row, dict):
                fieldnames.update(row.keys())
                
        fieldnames_list = sorted(list(fieldnames))
        
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames_list)
            writer.writeheader()
            for row in rows:
                if isinstance(row, dict):
                    writer.writerow(row)
                    
        print(f"Successfully exported lexicon to {csv_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    export_lexicon()
