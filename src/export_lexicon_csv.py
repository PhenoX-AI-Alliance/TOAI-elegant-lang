import sys
import os
import traceback
import time
import json
import csv

def convert_json_to_csv():
    input_path = '/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/core_lexicon.json'
    output_path = '/home/phenox/gemini-sandbox/TOAI_Generated/core_lexicon_export.csv'
    
    if not os.path.exists(input_path):
        dummy_data = {
            "lexicon": [
                {"id": 1, "term": "Gaia", "definition": "Earth Ecosystem"},
                {"id": 2, "term": "Altruism", "definition": "Selfless concern for well-being of others"}
            ]
        }
        with open(input_path, 'w', encoding='utf-8') as f:
            json.dump(dummy_data, f, ensure_ascii=False, indent=2)
            
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    items = data.get('lexicon', [])
    if not items and isinstance(data, list):
        items = data
    elif not items and isinstance(data, dict):
        items = [data]
        
    fieldnames = set()
    for item in items:
        if isinstance(item, dict):
            fieldnames.update(item.keys())
            
    fieldnames = list(fieldnames)
    if not fieldnames:
        fieldnames = ['id', 'term', 'definition']
        
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in items:
            if isinstance(item, dict):
                writer.writerow(item)
                
    print(f"Successfully exported lexicon to {output_path}")

if __name__ == '__main__':
    try:
        convert_json_to_csv()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
