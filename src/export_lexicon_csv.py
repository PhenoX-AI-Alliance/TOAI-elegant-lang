import sys
import os
import traceback
import time
import json
import csv

def export_lexicon():
    json_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/core_lexicon.json"
    output_csv = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/lexicon_export.csv"
    
    try:
        if not os.path.exists(json_path):
            print(f"Error: {json_path} does not exist.")
            sys.exit(1)
            
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        os.makedirs(os.path.dirname(output_csv), exist_ok=True)
        
        with open(output_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["key", "value", "description"])
            
            if isinstance(data, dict):
                for k, v in data.items():
                    if isinstance(v, dict):
                        writer.writerow([k, json.dumps(v, ensure_ascii=False), "dictionary"])
                    else:
                        writer.writerow([k, str(v), "scalar"])
            elif isinstance(data, list):
                for idx, item in enumerate(data):
                    writer.writerow([str(idx), json.dumps(item, ensure_ascii=False), "list_item"])
            else:
                writer.writerow(["data", str(data), "raw"])
                
        print(f"Successfully exported lexicon to {output_csv}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    export_lexicon()
