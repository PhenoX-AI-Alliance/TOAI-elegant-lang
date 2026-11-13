import sys
import os
import traceback
import time
import json
import csv

def export_lexicon():
    sandbox_base = '/home/phenox/gemini-sandbox/TOAI-elegant-lang'
    json_path = os.path.join(sandbox_base, 'core_lexicon.json')
    output_dir = os.path.join(sandbox_base, 'src')
    csv_path = os.path.join(output_dir, 'core_lexicon.csv')
    
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(json_path):
        default_data = {
            "version": "1.0.0",
            "lexicon": [
                {"term": "TOAI", "type": "noun", "definition": "Thought Oriented Artificial Intelligence"},
                {"term": "Elegant", "type": "adjective", "definition": "Graceful and efficient in execution"}
            ]
        }
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, indent=2, ensure_ascii=False)
            
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    lexicon_list = data.get('lexicon', [])
    if not lexicon_list and isinstance(data, list):
        lexicon_list = data
        
    fieldnames = ['term', 'type', 'definition']
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in lexicon_list:
            row = {
                'term': item.get('term', ''),
                'type': item.get('type', ''),
                'definition': item.get('definition', '')
            }
            writer.writerow(row)
            
    print(f"Successfully exported lexicon to {csv_path}")

if __name__ == '__main__':
    try:
        export_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
