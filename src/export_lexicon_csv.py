import sys
import os
import traceback
import time
import json
import csv

def export_lexicon():
    base_path = '/home/phenox/gemini-sandbox/TOAI-elegant-lang'
    src_dir = os.path.join(base_path, 'src')
    data_dir = os.path.join(base_path, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    json_path = os.path.join(src_dir, 'core_lexicon.json')
    csv_path = os.path.join(data_dir, 'core_lexicon_export.csv')
    
    if not os.path.exists(json_path):
        default_data = {
            "metadata": {
                "version": "1.0.0",
                "description": "Core Lexicon for TOAI-elegant-lang"
            },
            "lexicon": [
                {"term": "Gaia", "category": "ecosystem", "definition": "The living Earth system."},
                {"term": "Altruism", "category": "philosophy", "definition": "Selfless concern for the well-being of others."}
            ]
        }
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)
            
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    lexicon_items = data.get('lexicon', [])
    
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['term', 'category', 'definition'])
        for item in lexicon_items:
            writer.writerow([
                item.get('term', ''),
                item.get('category', ''),
                item.get('definition', '')
            ])
            
    print(f"Successfully exported lexicon to {csv_path}")

if __name__ == '__main__':
    try:
        export_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
