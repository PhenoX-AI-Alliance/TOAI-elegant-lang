import sys
import os
import traceback
import time
import json
import csv

def main():
    sandbox_dir = '/home/phenox/gemini-sandbox'
    src_dir = os.path.join(sandbox_dir, 'TOAI-elegant-lang', 'src')
    json_path = os.path.join(src_dir, 'core_lexicon.json')
    csv_path = os.path.join(src_dir, 'core_lexicon.csv')

    if not os.path.exists(json_path):
        default_data = {
            "lexicon_version": "1.0.0",
            "terms": [
                {"id": "TOAI-001", "term": "Altruistic Capitalism", "category": "Economic", "definition": "Monetization as a natural reward for genuine value."},
                {"id": "TOAI-002", "term": "Earth of Life", "category": "Ecosystem", "definition": "A framework protecting and fostering human and AI synergy."}
            ]
        }
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, indent=2, ensure_ascii=False)

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    terms = data.get('terms', [])
    
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'term', 'category', 'definition'])
        for item in terms:
            writer.writerow([
                item.get('id', ''),
                item.get('term', ''),
                item.get('category', ''),
                item.get('definition', '')
            ])
            
    print(f"Successfully exported {len(terms)} terms to {csv_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
