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
            print(f"Error: Input JSON file not found at {input_json_path}")
            sys.exit(1)
            
        with open(input_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        if isinstance(data, dict):
            items = data.get("lexicon", [])
            if not items:
                items = [data]
        elif isinstance(data, list):
            items = data
        else:
            items = [{"value": data}]
            
        fieldnames = set()
        for item in items:
            if isinstance(item, dict):
                fieldnames.update(item.keys())
                
        if not fieldnames:
            fieldnames = ["term", "definition"]
            
        fieldnames = sorted(list(fieldnames))
        
        with open(output_csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in items:
                if isinstance(item, dict):
                    row = {k: str(item.get(k, "")) for k in fieldnames}
                    writer.writerow(row)
                else:
                    writer.writerow({fieldnames[0]: str(item)})
                    
        print(f"Successfully exported lexicon to {output_csv_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
