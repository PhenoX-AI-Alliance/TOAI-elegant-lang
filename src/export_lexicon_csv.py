import sys
import os
import traceback
import time
import json
import csv

def main():
    try:
        sandbox_dir = '/home/phenox/gemini-sandbox'
        lexicon_json_path = os.path.join(sandbox_dir, 'TOAI-elegant-lang', 'core_lexicon.json')
        output_csv_path = os.path.join(sandbox_dir, 'TOAI-elegant-lang', 'lexicon_export.csv')
        
        os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
        
        if not os.path.exists(lexicon_json_path):
            print(f"Error: {lexicon_json_path} does not exist.")
            sys.exit(1)
            
        with open(lexicon_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        items = []
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            items = [data]
        else:
            print("Error: Unsupported JSON structure for CSV export.")
            sys.exit(1)
            
        fieldnames = set()
        for item in items:
            if isinstance(item, dict):
                fieldnames.update(item.keys())
                
        fieldnames_list = sorted(list(fieldnames))
        if not fieldnames_list:
            fieldnames_list = ['key', 'value']
            
        with open(output_csv_path, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames_list)
            writer.writeheader()
            for item in items:
                if isinstance(item, dict):
                    row = {k: str(item.get(k, '')) for k in fieldnames_list}
                    writer.writerow(row)
                else:
                    writer.writerow({fieldnames_list[0]: str(item)})
                    
        print(f"Successfully exported lexicon to {output_csv_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
