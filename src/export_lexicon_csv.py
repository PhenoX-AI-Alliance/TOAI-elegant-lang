import sys
import os
import traceback
import time
import json
import csv

def convert_json_to_csv():
    target_dir = '/home/phenox/gemini-sandbox/TOAI-elegant-lang/src'
    json_path = os.path.join(target_dir, 'core_lexicon.json')
    csv_path = os.path.join(target_dir, 'core_lexicon.csv')
    
    if not os.path.exists(json_path):
        print(f"Error: {json_path} does not exist. Creating a default one.")
        default_data = {
            "version": "1.0.0",
            "terms": [
                {"id": "gaia_01", "term": "Gaia Ecosystem", "category": "Core", "description": "The Earth of Life ecosystem."},
                {"id": "gaia_02", "term": "Altruistic Monetization", "category": "Economy", "description": "Generating sustainable value through altruism."}
            ]
        }
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)
            
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    terms = data.get('terms', [])
    
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Term', 'Category', 'Description'])
        for item in terms:
            writer.writerow([
                item.get('id', ''),
                item.get('term', ''),
                item.get('category', ''),
                item.get('description', '')
            ])
            
    print(f"Successfully exported lexicon to {csv_path}")

if __name__ == '__main__':
    try:
        convert_json_to_csv()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
