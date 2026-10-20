import sys
import os
import traceback
import time
import json
import csv

def main():
    input_json_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/core_lexicon.json"
    output_csv_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/core_lexicon.csv"
    
    try:
        if not os.path.exists(input_json_path):
            print(f"Error: Input JSON not found at {{input_json_path}}")
            sys.exit(1)
            
        with open(input_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        if isinstance(data, dict):
            rows = []
            for key, value in data.items():
                if isinstance(value, dict):
                    row = {"key": key}
                    row.update(value)
                    rows.append(row)
                else:
                    rows.append({"key": key, "value": str(value)})
        elif isinstance(data, list):
            rows = data
        else:
            print("Error: Unsupported JSON root type for CSV export.")
            sys.exit(1)
            
        if not rows:
            print("Warning: No data found to export.")
            fieldnames = ["key"]
        else:
            fieldnames = list(rows[0].keys())
            
        with open(output_csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
                
        print(f"Successfully exported lexicon to {{output_csv_path}}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
