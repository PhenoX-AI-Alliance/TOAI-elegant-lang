import sys
import os
import traceback
import time
import json
import csv

def convert_lexicon_to_csv():
    base_dir = '/home/phenox/gemini-sandbox/TOAI-elegant-lang'
    src_dir = os.path.join(base_dir, 'src')
    data_dir = os.path.join(base_dir, 'data')
    
    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)
    
    json_path = os.path.join(data_dir, 'core_lexicon.json')
    csv_path = os.path.join(data_dir, 'core_lexicon.csv')
    
    if not os.path.exists(json_path):
        dummy_data = [
            {"term": "Gaia", "category": "ecosystem", "definition": "The living Earth system."},
            {"term": "Altruism", "category": "philosophy", "definition": "Selfless concern for the well-being of others."}
        ]
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(dummy_data, f, indent=2, ensure_ascii=False)
            
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    if not isinstance(data, list):
        data = [data]
        
    fieldnames = set()
    for item in data:
        if isinstance(item, dict):
            fieldnames.update(item.keys())
            
    fieldnames = list(fieldnames)
    if not fieldnames:
        fieldnames = ['term', 'category', 'definition']
        
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            if isinstance(item, dict):
                writer.writerow(item)
                
    print(f"Successfully exported {json_path} to {csv_path}")

if __name__ == '__main__':
    try:
        convert_lexicon_to_csv()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
