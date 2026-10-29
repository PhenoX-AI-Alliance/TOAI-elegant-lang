import sys
import os
import json
import csv
import traceback

def export_lexicon():
    try:
        base_dir = '/home/phenox/gemini-sandbox/TOAI-elegant-lang/src'
        json_path = os.path.join(base_dir, 'core_lexicon.json')
        csv_path = os.path.join(base_dir, 'core_lexicon.csv')
        
        if not os.path.exists(json_path):
            print(f"Error: {json_path} not found.")
            sys.exit(1)
            
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if not isinstance(data, (list, dict)):
            print("Error: Invalid JSON format, expected list or dict.")
            sys.exit(1)
            
        if isinstance(data, dict):
            data = [data]
            
        fieldnames = set()
        for item in data:
            if isinstance(item, dict):
                fieldnames.update(item.keys())
            else:
                print(f"Warning: Skipping non-dict item: {type(item)}")
                
        fieldnames = list(fieldnames)
        if not fieldnames:
            fieldnames = ['term', 'value']
            
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in data:
                if isinstance(item, dict):
                    row = {k: item.get(k, '') for k in fieldnames}
                    writer.writerow(row)
                    
        print(f"Successfully exported lexicon to {csv_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    export_lexicon()
