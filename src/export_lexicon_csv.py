import sys
import os
import traceback
import time
import json
import csv

def convert_lexicon_to_csv():
    target_dir = '/home/phenox/gemini-sandbox/TOAI-elegant-lang'
    json_path = os.path.join(target_dir, 'core_lexicon.json')
    csv_path = os.path.join(target_dir, 'core_lexicon.csv')
    
    try:
        if not os.path.exists(json_path):
            print(f"Error: {json_path} does not exist.")
            sys.exit(1)
            
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if isinstance(data, dict):
            items = data.items()
        elif isinstance(data, list):
            items = enumerate(data)
        else:
            print("Error: Unsupported JSON root structure.")
            sys.exit(1)
            
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Key_Or_Index', 'Value'])
            for k, v in items:
                if isinstance(v, (dict, list)):
                    v_str = json.dumps(v, ensure_ascii=False)
                else:
                    v_str = str(v)
                writer.writerow([str(k), v_str])
                
        print(f"Successfully exported lexicon to {csv_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    convert_lexicon_to_csv()
