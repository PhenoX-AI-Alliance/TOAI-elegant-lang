import sys
import os
import traceback
import time
import json
import csv

def convert_json_to_csv():
    target_dir = '/home/phenox/gemini-sandbox/TOAI-elegant-lang'
    json_path = os.path.join(target_dir, 'core_lexicon.json')
    csv_path = os.path.join(target_dir, 'core_lexicon.csv')
    
    if not os.path.exists(json_path):
        print(f"Error: {json_path} does not exist.")
        sys.exit(1)
        
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Failed to parse JSON: {e}")
        traceback.print_exc()
        sys.exit(1)
        
    try:
        items = []
        if isinstance(data, dict):
            items = data.get('lexicon', data.get('items', []))
            if not items:
                items = [data]
        elif isinstance(data, list):
            items = data
        else:
            items = [{'value': str(data)}]
            
        fieldnames = set()
        for item in items:
            if isinstance(item, dict):
                fieldnames.update(item.keys())
                
        if not fieldnames:
            fieldnames = {'term', 'definition'}
            
        fieldnames_list = sorted(list(fieldnames))
        
        with open(csv_path, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames_list)
            writer.writeheader()
            for item in items:
                if isinstance(item, dict):
                    row = {k: str(item.get(k, '')) for k in fieldnames_list}
                    writer.writerow(row)
                else:
                    writer.writerow({fieldnames_list[0]: str(item)})
                    
        print(f"Successfully exported lexicon to {csv_path}")
    except Exception as e:
        print(f"Failed to export CSV: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    try:
        convert_json_to_csv()
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()
        sys.exit(1)
