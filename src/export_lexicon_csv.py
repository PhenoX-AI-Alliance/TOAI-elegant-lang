import sys
import os
import traceback
import time
import json
import csv

def main():
    sandbox_dir = "/home/phenox/gemini-sandbox"
    json_path = os.path.join(sandbox_dir, "TOAI-elegant-lang", "src", "core_lexicon.json")
    output_dir = os.path.join(sandbox_dir, "TOAI_Generated")
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, "core_lexicon_export.csv")
    
    if not os.path.exists(json_path):
        print(f"Error: {json_path} does not exist.")
        sys.exit(1)
        
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Failed to load JSON: {e}")
        traceback.print_exc()
        sys.exit(1)
        
    items = []
    if isinstance(data, dict):
        lexicon_data = data.get("lexicon", data)
        if isinstance(lexicon_data, list):
            items = lexicon_data
        elif isinstance(lexicon_data, dict):
            for k, v in lexicon_data.items():
                if isinstance(v, dict):
                    v["key"] = k
                    items.append(v)
                else:
                    items.append({"key": k, "value": v})
    elif isinstance(data, list):
        items = data
    else:
        print("Error: Unknown JSON structure.")
        sys.exit(1)
        
    fieldnames = set()
    for item in items:
        if isinstance(item, dict):
            for k in item.keys():
                fieldnames.add(k)
                
    fieldnames = list(fieldnames)
    if not fieldnames:
        fieldnames = ["key", "value"]
        
    try:
        with open(csv_path, "w", encoding="utf-8", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item in items:
                if isinstance(item, dict):
                    row = {k: str(item.get(k, "")) for k in fieldnames}
                    writer.writerow(row)
                else:
                    writer.writerow({fieldnames[0]: str(item)})
                    
        print(f"Successfully exported lexicon CSV to {csv_path}")
    except Exception as e:
        print(f"Failed to write CSV: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Fatal error: {e}")
        traceback.print_exc()
        sys.exit(1)