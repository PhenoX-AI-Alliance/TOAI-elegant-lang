# -*- coding: utf-8 -*-
import sys
import os
import json
import csv
import traceback

def export_lexicon():
    input_path = '/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/core_lexicon.json'
    output_path = '/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/core_lexicon.csv'
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} does not exist.")
        sys.exit(1)
        
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        rows = []
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    row = {'key': key}
                    row.update(value)
                    rows.append(row)
                else:
                    rows.append({'key': key, 'value': str(value)})
        elif isinstance(data, list):
            rows = data
        else:
            print("Error: Unsupported JSON structure for CSV export.")
            sys.exit(1)
            
        if not rows:
            print("Warning: No data found to export.")
            fieldnames = ['key']
        else:
            fieldnames = list(rows[0].keys())
            
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
                
        print(f"Successfully exported lexicon to {output_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    export_lexicon()
