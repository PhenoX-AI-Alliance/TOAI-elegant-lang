import sys
import os
import traceback
import time
import json
import csv

def export_lexicon():
    source_json = '/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/core_lexicon.json'
    output_csv = '/home/phenox/gemini-sandbox/TOAI_Generated/core_lexicon_export.csv'
    
    if not os.path.exists(source_json):
        print(f"Error: Source JSON not found at {source_json}")
        sys.exit(1)
        
    with open(source_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    if isinstance(data, dict):
        rows = []
        for k, v in data.items():
            if isinstance(v, dict):
                row = {'key': k}
                row.update(v)
                rows.append(row)
            else:
                rows.append({'key': k, 'value': v})
    elif isinstance(data, list):
        rows = data
    else:
        print("Error: Unsupported JSON structure for CSV export.")
        sys.exit(1)
        
    if not rows:
        print("Warning: No data rows found to export.")
        fieldnames = ['key', 'value']
    else:
        fieldnames = list(rows[0].keys())
        
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
            
    print(f"Successfully exported lexicon to {output_csv}")

if __name__ == '__main__':
    try:
        export_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
