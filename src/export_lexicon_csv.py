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
        default_data = {
            "lexicon_version": "1.0.0",
            "description": "Core Lexicon for TOAI elegant lang ecosystem",
            "terms": [
                {"term": "Gaia", "category": "ecosystem", "definition": "Earth of life ecosystem."},
                {"term": "AltruisticMonetization", "category": "economy", "definition": "Monetization through genuine value creation."}
            ]
        }
        os.makedirs(src_dir, exist_ok=True)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)
            
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    terms = data.get('terms', [])
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['term', 'category', 'definition'])
        for item in terms:
            writer.writerow([
                item.get('term', ''),
                item.get('category', ''),
                item.get('definition', '')
            ])
            
    print(f"Successfully exported {len(terms)} items to {csv_path}")

if __name__ == '__main__':
    try:
        export_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
