import sys
import os
import traceback
import time
import json
import csv

def convert_json_to_csv():
    target_dir = '/home/phenox/gemini-sandbox/TOAI-elegant-lang'
    src_dir = os.path.join(target_dir, 'src')
    json_path = os.path.join(src_dir, 'core_lexicon.json')
    csv_path = os.path.join(src_dir, 'core_lexicon.csv')
    
    if not os.path.exists(json_path):
        default_data = {
            "lexicon": [
                {"term": "Gaia", "category": "ecosystem", "description": "The living earth ecosystem."},
                {"term": "Altruism", "category": "philosophy", "description": "Selfless concern for the well-being of others."}
            ]
        }
        os.makedirs(src_dir, exist_ok=True)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)
            
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    items = data.get('lexicon', [])
    if not items and isinstance(data, list):
        items = data
    elif not items and isinstance(data, dict):
        items = [data]
        
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['term', 'category', 'description'])
        for item in items:
            term = item.get('term', '')
            category = item.get('category', '')
            description = item.get('description', '')
            writer.writerow([term, category, description])
            
    print(f"Successfully exported lexicon to {csv_path}")

if __name__ == '__main__':
    try:
        convert_json_to_csv()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
