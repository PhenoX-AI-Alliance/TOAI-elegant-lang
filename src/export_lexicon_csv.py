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
            print(f"Error: {lexicon_json_path} does not exist.", file=sys.stderr)
            sys.exit(1)
            
        with open(lexicon_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        entries = []
        if isinstance(data, dict):
            for key, val in data.items():
                if isinstance(val, dict):
                    row = {'key': key}
                    row.update(val)
                    entries.append(row)
                else:
                    entries.append({'key': key, 'value': val})
        elif isinstance(data, list):
            entries = data
        else:
            print("Error: Unsupported JSON format in core_lexicon.json", file=sys.stderr)
            sys.exit(1)
            
        if not entries:
            print("Warning: No entries found in core_lexicon.json", file=sys.stderr)
            fieldnames = ['key']
        else:
            fieldnames = sorted(list(set(k for entry in entries for k in entry.keys())))
            
        with open(output_csv_path, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for entry in entries:
                writer.writerow(entry)
                
        print(f"Successfully exported {len(entries)} entries to {output_csv_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
