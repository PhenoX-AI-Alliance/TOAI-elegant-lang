import sys
import os
import traceback
import time
import json
import csv

def main():
    try:
        base_dir = '/home/phenox/gemini-sandbox/TOAI-elegant-lang'
        json_path = os.path.join(base_dir, 'core_lexicon.json')
        output_csv_path = os.path.join(base_dir, 'core_lexicon.csv')
        
        if not os.path.exists(json_path):
            print(f"Error: {json_path} does not exist.", file=sys.stderr)
            sys.exit(1)
            
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
            print("Error: Unsupported JSON format for CSV export.", file=sys.stderr)
            sys.exit(1)
            
        if not rows:
            print("Warning: No data found to export.", file=sys.stderr)
            fieldnames = ['key']
        else:
            fieldnames = list(rows[0].keys())
            
        with open(output_csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
                
        print(f"Successfully exported {json_path} to {output_csv_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
