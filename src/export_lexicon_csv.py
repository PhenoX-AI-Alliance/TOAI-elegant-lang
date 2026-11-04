import sys
import os
import traceback
import time
import json
import csv

def convert_lexicon():
    json_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/core_lexicon.json"
    csv_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/core_lexicon.csv"
    
    if not os.path.exists(json_path):
        print(f"Error: {json_path} does not exist.")
        sys.exit(1)
        
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        rows = []
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    row = {"key": key}
                    row.update(value)
                    rows.append(row)
                else:
                    rows.append({"key": key, "value": value})
        elif isinstance(data, list):
            rows = data
        else:
            print("Error: Unsupported JSON structure.")
            sys.exit(1)
            
        if not rows:
            print("Warning: No data found to export.")
            return
            
        fieldnames = set()
        for row in rows:
            if isinstance(row, dict):
                fieldnames.update(row.keys())
        fieldnames = sorted(list(fieldnames))
        
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                if isinstance(row, dict):
                    writer.writerow(row)
                    
        print(f"Successfully exported lexicon to {csv_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    convert_lexicon()
