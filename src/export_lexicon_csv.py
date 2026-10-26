import sys
import os
import traceback
import json
import csv

def export_lexicon():
    base_dir = '/home/phenox/gemini-sandbox/TOAI-elegant-lang'
    json_path = os.path.join(base_dir, 'core_lexicon.json')
    csv_path = os.path.join(base_dir, 'core_lexicon.csv')
    
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
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['key', 'value', 'description'])
            if isinstance(data, dict):
                for k, v in data.items():
                    if isinstance(v, dict):
                        desc = v.get('description', '')
                        val = v.get('value', str(v))
                        writer.writerow([k, val, desc])
                    else:
                        writer.writerow([k, str(v), ''])
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        k = item.get('key', '')
                        v = item.get('value', '')
                        desc = item.get('description', '')
                        writer.writerow([k, v, desc])
                    else:
                        writer.writerow(['', str(item), ''])
        print(f"Successfully exported lexicon to {csv_path}")
    except Exception as e:
        print(f"Failed to write CSV: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    export_lexicon()
