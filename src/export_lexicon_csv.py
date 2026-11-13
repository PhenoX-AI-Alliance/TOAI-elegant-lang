import sys
import os
import traceback
import time
import json
import csv

def export_lexicon():
    base_path = '/home/phenox/gemini-sandbox/TOAI-elegant-lang'
    core_json_path = os.path.join(base_path, 'core_lexicon.json')
    output_dir = os.path.join(base_path, 'src')
    output_csv_path = os.path.join(output_dir, 'core_lexicon.csv')

    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(core_json_path):
        print(f"Error: {core_json_path} does not exist.")
        sys.exit(1)

    try:
        with open(core_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Failed to parse JSON: {e}")
        traceback.print_exc()
        sys.exit(1)

    items = []
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                row = {'key': key}
                row.update(value)
                items.append(row)
            else:
                items.append({'key': key, 'value': value})
    elif isinstance(data, list):
        items = data
    else:
        print("Error: Unsupported JSON root structure.")
        sys.exit(1)

    fieldnames = set()
    for item in items:
        if isinstance(item, dict):
            fieldnames.update(item.keys())
    
    fieldnames = sorted(list(fieldnames))

    try:
        with open(output_csv_path, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item in items:
                if isinstance(item, dict):
                    writer.writerow(item)
        print(f"Successfully exported lexicon to {output_csv_path}")
    except Exception as e:
        print(f"Failed to write CSV: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    try:
        export_lexicon()
    except Exception as e:
        print(f"Critical error: {e}")
        traceback.print_exc()
        sys.exit(1)
