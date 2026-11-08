import sys
import os
import traceback
import time
import json
import csv

def export_lexicon():
    base_path = '/home/phenox/gemini-sandbox'
    input_json_path = os.path.join(base_path, 'TOAI-elegant-lang', 'data', 'core_lexicon.json')
    output_csv_path = os.path.join(base_path, 'TOAI-elegant-lang', 'data', 'core_lexicon.csv')
    
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    
    if not os.path.exists(input_json_path):
        default_data = [
            {"term": "Gaia", "category": "ecosystem", "description": "The living Earth ecosystem."},
            {"term": "Altruism", "category": "philosophy", "description": "Selfless concern for the well-being of others."}
        ]
        os.makedirs(os.path.dirname(input_json_path), exist_ok=True)
        with open(input_json_path, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)
            
    with open(input_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    if not isinstance(data, list):
        if isinstance(data, dict):
            data = [data]
        else:
            data = []
            
    fieldnames = set()
    for item in data:
        if isinstance(item, dict):
            fieldnames.update(item.keys())
            
    fieldnames = sorted(list(fieldnames))
    if not fieldnames:
        fieldnames = ['term', 'category', 'description']
        
    with open(output_csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            if isinstance(item, dict):
                writer.writerow(item)
                
    print(f"Successfully exported lexicon to {output_csv_path}")

if __name__ == '__main__':
    try:
        export_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
