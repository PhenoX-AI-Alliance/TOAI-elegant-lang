import sys
import os
import json
import csv

def export_lexicon():
    base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
    input_path = os.path.join(base_dir, "data", "core_lexicon.json")
    output_path = os.path.join(base_dir, "data", "core_lexicon.csv")
    
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
        
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    fieldnames = set()
    for item in data:
        if isinstance(item, dict):
            fieldnames.update(item.keys())
    fieldnames = sorted(list(fieldnames))
    
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            row = {}
            for key in fieldnames:
                val = item.get(key, "")
                if isinstance(val, (list, dict)):
                    val = json.dumps(val, ensure_ascii=False)
                row[key] = val
            writer.writerow(row)
    print(f"Successfully exported lexicon to {output_path}")

if __name__ == "__main__":
    export_lexicon()
