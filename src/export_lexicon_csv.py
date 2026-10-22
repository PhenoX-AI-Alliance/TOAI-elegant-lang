import sys
import os
import traceback
import time
import json
import csv

def convert_lexicon():
    base_dir = '/home/phenox/gemini-sandbox/TOAI-elegant-lang'
    json_path = os.path.join(base_dir, 'core_lexicon.json')
    csv_path = os.path.join(base_dir, 'core_lexicon.csv')
    
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        sys.exit(1)
        
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        rows = []
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    rows.append(item)
        elif isinstance(data, dict):
            for key, val in data.items():
                if isinstance(val, dict):
                    row = val.copy()
                    row['key'] = key
                    rows.append(row)
                else:
                    rows.append({'key': key, 'value': val})
                    
        if not rows:
            print("Warning: No valid rows found in JSON to export.")
            return
            
        fieldnames = set()
        for row in rows:
            fieldnames.update(row.keys())
        fieldnames = list(fieldnames)
        
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
                
        print(f"Successfully exported lexicon to {csv_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    convert_lexicon()
