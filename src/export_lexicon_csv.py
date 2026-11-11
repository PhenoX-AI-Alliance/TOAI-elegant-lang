import sys
import os
import json
import csv

def export_lexicon():
    json_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/core_lexicon.json"
    csv_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/core_lexicon.csv"
    
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Missing {json_path}")
        
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    rows = []
    if isinstance(data, dict):
        if "entries" in data and isinstance(data["entries"], list):
            rows = data["entries"]
        else:
            for k, v in data.items():
                if isinstance(v, dict):
                    r = {"key": k}
                    r.update(v)
                    rows.append(r)
                else:
                    rows.append({"key": k, "value": v})
    elif isinstance(data, list):
        rows = data
        
    if not rows:
        raise ValueError("Invalid or empty core_lexicon.json structure")
        
    fieldnames = set()
    for row in rows:
        if isinstance(row, dict):
            fieldnames.update(row.keys())
            
    fieldnames_list = sorted(list(fieldnames))
    if not fieldnames_list:
        fieldnames_list = ["term", "definition"]
        
    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames_list)
        writer.writeheader()
        for row in rows:
            if isinstance(row, dict):
                writer.writerow(row)
            else:
                writer.writerow({"value": str(row)})
                
    print(f"Successfully exported {len(rows)} entries to {csv_path}")

if __name__ == "__main__":
    export_lexicon()
