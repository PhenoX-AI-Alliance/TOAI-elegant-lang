import sys
import os
import traceback
import json
import csv

def export_lexicon():
    source_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/core_lexicon.json"
    output_path = "/home/phenox/gemini-sandbox/TOAI_Generated/core_lexicon_export.csv"
    
    if not os.path.exists(source_path):
        print(f"Error: {source_path} does not exist.")
        sys.exit(1)
        
    try:
        with open(source_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        rows = []
        if isinstance(data, dict):
            for key, val in data.items():
                if isinstance(val, dict):
                    row = {"term": key}
                    row.update(val)
                    rows.append(row)
                else:
                    rows.append({"term": key, "value": val})
        elif isinstance(data, list):
            rows = data
        else:
            print("Error: Unsupported JSON structure for CSV export.")
            sys.exit(1)
            
        if not rows:
            print("Warning: No data found to export.")
            return
            
        fieldnames = set()
        for row in rows:
            if isinstance(row, dict):
                fieldnames.update(row.keys())
                
        fieldnames = list(fieldnames)
        
        with open(output_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                if isinstance(row, dict):
                    writer.writerow(row)
                    
        print(f"Successfully exported lexicon to {output_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    export_lexicon()
