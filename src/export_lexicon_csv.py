import sys
import os
import traceback
import time
import json
import csv

def main():
    try:
        base_dir = '/home/phenox/gemini-sandbox'
        lexicon_json_path = os.path.join(base_dir, 'TOAI-elegant-lang', 'src', 'core_lexicon.json')
        output_csv_path = os.path.join(base_dir, 'TOAI-elegant-lang', 'src', 'core_lexicon.csv')
        
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
            print("Warning: No data to export.")
            fieldnames = ['key']
        else:
            fieldnames = list(set().union(*(d.keys() for d in rows)))
            
        with open(output_csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
                
        print(f"Successfully exported {lexicon_json_path} to {output_csv_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
