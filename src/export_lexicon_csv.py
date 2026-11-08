import sys
import os
import traceback
import time
import json
import csv

def export_lexicon():
    base_dir = '/home/phenox/gemini-sandbox/TOAI-elegant-lang'
    src_dir = os.path.join(base_dir, 'src')
    json_path = os.path.join(src_dir, 'core_lexicon.json')
    csv_path = os.path.join(src_dir, 'core_lexicon.csv')
    
    if not os.path.exists(json_path):
        default_data = [
            {"id": 1, "term": "Gaia", "category": "ecosystem", "description": "The living Earth system."},
            {"id": 2, "term": "Altruism", "category": "philosophy", "description": "Selfless concern for the well-being of others."}
        ]
        os.makedirs(src_dir, exist_ok=True)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)
            
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    if not isinstance(data, list):
        data = [data]
        
    if not data:
        print("No data found in core_lexicon.json")
        return
        
    fieldnames = list(data[0].keys())
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
            
    print(f"Successfully exported {len(data)} records to {csv_path}")

if __name__ == '__main__':
    try:
        export_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
