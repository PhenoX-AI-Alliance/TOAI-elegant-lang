import sys
import os
import traceback
import time
import json
import csv

def main():
    input_path = '/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/core_lexicon.json'
    output_path = '/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/core_lexicon.csv'
    
    if not os.path.exists(input_path):
        sample_data = {
            "lexicon": [
                {"id": "1", "term": "TOAI", "definition": "Toward Open Artificial Intelligence"},
                {"id": "2", "term": "Elegance", "definition": "Simplicity combined with power"}
            ]
        }
        os.makedirs(os.path.dirname(input_path), exist_ok=True)
        with open(input_path, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, ensure_ascii=False, indent=2)

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
            
    fieldnames = sorted(list(fieldnames))
    if not fieldnames:
        fieldnames = ['id', 'term', 'definition']

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in items:
            if isinstance(item, dict):
                writer.writerow(item)
                
    print(f"Successfully exported {len(items)} items to {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
