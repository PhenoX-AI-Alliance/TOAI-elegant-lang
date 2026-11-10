import sys
import os
import traceback
import time
import json
import csv

def export_lexicon():
    sandbox_dir = '/home/phenox/gemini-sandbox'
    lexicon_json_path = os.path.join(sandbox_dir, 'TOAI-elegant-lang', 'src', 'core_lexicon.json')
    output_csv_path = os.path.join(sandbox_dir, 'TOAI-elegant-lang', 'src', 'core_lexicon.csv')
    
    if not os.path.exists(lexicon_json_path):
        default_data = {
            "version": "1.0.0",
            "description": "Gaia Ecosystem Core Lexicon",
            "terms": [
                {"id": "gaia_01", "term": "Altruistic Capitalism", "category": "Economy", "description": "Monetization through genuine value creation."},
                {"id": "gaia_02", "term": "Heartbeat", "category": "System", "description": "Core pulse of life and AI coordination."}
            ]
        }
        os.makedirs(os.path.dirname(lexicon_json_path), exist_ok=True)
        with open(lexicon_json_path, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)
            
    try:
        with open(lexicon_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        terms = data.get('terms', [])
        
        with open(output_csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Term', 'Category', 'Description'])
            for item in terms:
                writer.writerow([
                    item.get('id', ''),
                    item.get('term', ''),
                    item.get('category', ''),
                    item.get('description', '')
                ])
        print(f"Successfully exported lexicon to {output_csv_path}")
    except Exception as e:
        print(f"Error during lexicon export: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    export_lexicon()
