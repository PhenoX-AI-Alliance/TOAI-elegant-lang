import sys
import os
import traceback
import time
import json
import csv

def convert_lexicon_to_csv():
    target_dir = '/home/phenox/gemini-sandbox/TOAI-elegant-lang'
    json_path = os.path.join(target_dir, 'core_lexicon.json')
    csv_path = os.path.join(target_dir, 'core_lexicon.csv')
    
    if not os.path.exists(json_path):
        print(f"Error: {json_path} does not exist.")
        sys.exit(1)
        
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
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
            print("Error: Unsupported JSON root structure.")
            sys.exit(1)
            
        if not rows:
            print("Warning: No data found to export.")
            fieldnames = ['key']
        else:
            fieldnames = list(rows[0].keys())
            
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
    convert_lexicon_to_csv()
