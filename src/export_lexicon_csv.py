import sys
import os
import traceback
import time
import json
import csv

def main():
    try:
        input_path = '/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/core_lexicon.json'
        output_path = '/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/core_lexicon.csv'
        
        if not os.path.exists(input_path):
            print(f"Error: Input file {input_path} not found.")
            sys.exit(1)
            
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if isinstance(data, dict):
            rows = []
            for key, value in data.items():
                if isinstance(value, dict):
                    row = {'key': key}
                    row.update(value)
                    rows.append(row)
                else:
                    rows.append({'key': key, 'value': value})
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
                
        fieldnames = list(fieldnames)
        
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                if isinstance(row, dict):
                    writer.writerow(row)
                    
        print(f"Successfully exported lexicon to {output_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()\n