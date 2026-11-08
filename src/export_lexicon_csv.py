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
    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)
    
    json_path = os.path.join(data_dir, 'core_lexicon.json')
    csv_path = os.path.join(data_dir, 'core_lexicon.csv')
    
    if not os.path.exists(json_path):
        sample_data = {
            "version": "1.0.0",
            "terms": [
                {"id": "gaia_001", "name": "Gaia Ecosystem", "category": "core", "description": "Earth of life and altruistic intelligence."},
                {"id": "gaia_002", "name": "Altruistic Monetization", "category": "economy", "description": "Fair reward for genuine value creation."}
            ]
        }
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, indent=2, ensure_ascii=False)
            
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    terms = data.get('terms', [])
    
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Name', 'Category', 'Description'])
        for term in terms:
            writer.writerow([
                term.get('id', ''),
                term.get('name', ''),
                term.get('category', ''),
                term.get('description', '')
            ])
            
    print(f"Successfully exported lexicon to {csv_path}")

if __name__ == '__main__':
    try:
        export_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
