import sys
import os
import traceback
import time
import json
import csv

def export_lexicon():
    base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
    json_path = os.path.join(base_dir, "core_lexicon.json")
    if not os.path.exists(json_path):
        json_path = os.path.join(base_dir, "src", "core_lexicon.json")
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"core_lexicon.json not found in {base_dir}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    entries = []
    if isinstance(data, list):
        entries = data
    elif isinstance(data, dict):
        if "lexicon" in data and isinstance(data["lexicon"], list):
            entries = data["lexicon"]
        else:
            for k, v in data.items():
                if isinstance(v, list):
                    entries = v
                    break
            if not entries:
                entries = [data]
    else:
        raise ValueError("Invalid core_lexicon.json format.")

    if not entries:
        raise ValueError("Empty core_lexicon.json data.")

    csv_path = os.path.join(base_dir, "src", "core_lexicon.csv")
    fields = set()
    for entry in entries:
        if isinstance(entry, dict):
            fields.update(entry.keys())
    
    fieldnames = sorted(list(fields))
    if not fieldnames:
        fieldnames = ["term", "definition", "category"]

    with open(csv_path, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in entries:
            if isinstance(entry, dict):
                row = {field: entry.get(field, "") for field in fieldnames}
                writer.writerow(row)
            else:
                writer.writerow({fieldnames[0]: str(entry)})

    print(f"Successfully exported lexicon to {csv_path}")

if __name__ == "__main__":
    try:
        export_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
