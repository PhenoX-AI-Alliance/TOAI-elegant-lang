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
        output_csv_path = os.path.join(sandbox_dir, 'TOAI-elegant-lang', 'core_lexicon.csv')
        
        if not os.path.exists(lexicon_json_path):
            print(f"Error: {lexicon_json_path} does not exist.")
            sys.exit(1)
            
        with open(lexicon_json_path, 'r', encoding='utf-8') as f:
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
            print("Error: No data found to export.")
            sys.exit(1)
            
        fieldnames = set()
        for row in rows:
            if isinstance(row, dict):
                fieldnames.update(row.keys())
                
        fieldnames_list = sorted(list(fieldnames))
        
        os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
        with open(output_csv_path, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames_list)
            writer.writeheader()
            for row in rows:
                if isinstance(row, dict):
                    writer.writerow(row)
                    
        print(f"Successfully exported lexicon to {output_csv_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
