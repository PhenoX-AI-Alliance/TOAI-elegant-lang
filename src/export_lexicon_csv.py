import sys
import os
import json
import csv

def export_lexicon():
    base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src"
    json_path = os.path.join(base_dir, "core_lexicon.json")
    csv_path = os.path.join(base_dir, "core_lexicon.csv")
    
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"core_lexicon.json not found at {json_path}")
        
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    entries = []
    if isinstance(data, dict):
        if "entries" in data and isinstance(data["entries"], list):
            entries = data["entries"]
        else:
            for k, v in data.items():
                if isinstance(v, dict):
                    item = v.copy()
                    item["key"] = k
                    entries.append(item)
                else:
                    entries.append({"term": k, "definition": str(v)})
    elif isinstance(data, list):
        entries = data
        
    if not entries:
        raise ValueError("Invalid or empty core_lexicon.json format.")
        
    fieldnames = set()
    for entry in entries:
        if isinstance(entry, dict):
            fieldnames.update(entry.keys())
            
    fieldnames_list = sorted(list(fieldnames))
    if not fieldnames_list:
        fieldnames_list = ["term", "definition"]
        
    with open(csv_path, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames_list)
        writer.writeheader()
        for entry in entries:
            if isinstance(entry, dict):
                row = {k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in entry.items()}
                writer.writerow(row)
            else:
                writer.writerow({"definition": str(entry)})
                
    print(f"Successfully exported lexicon to {csv_path}")

if __name__ == "__main__":
    export_lexicon()
