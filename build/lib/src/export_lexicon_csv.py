import sys
import os
import traceback
import time
import json
import csv

def main():
    try:
        input_json_path = '/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/core_lexicon.json'
        output_csv_path = '/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/core_lexicon.csv'
        
        if not os.path.exists(input_json_path):
            print(f"Error: {input_json_path} does not exist.", file=sys.stderr)
            sys.exit(1)
            
        with open(input_json_path, 'r', encoding='utf-8') as f:
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
            print("Error: Unsupported JSON structure for CSV export.", file=sys.stderr)
            sys.exit(1)
            
        fieldnames = set()
        for row in rows:
            if isinstance(row, dict):
                fieldnames.update(row.keys())
        fieldnames = sorted(list(fieldnames))
        
        with open(output_csv_path, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                if isinstance(row, dict):
                    writer.writerow(row)
                    
        print(f"Successfully exported {output_csv_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
