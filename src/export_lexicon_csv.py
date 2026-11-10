import sys
import os
import traceback
import time
import json
import csv

def main():
    sandbox_dir = '/home/phenox/gemini-sandbox'
    lexicon_json_path = os.path.join(sandbox_dir, 'TOAI-elegant-lang', 'core_lexicon.json')
    output_csv_path = os.path.join(sandbox_dir, 'TOAI-elegant-lang', 'core_lexicon.csv')
    
    try:
        if not os.path.exists(lexicon_json_path):
            default_data = {
                "version": "1.0.0",
                "description": "Core lexicon for TOAI-elegant-lang",
                "terms": [
                    {"term": "Gaia", "category": "ecosystem", "meaning": "Earth of Life ecosystem core"},
                    {"term": "AltruisticMonetization", "category": "economy", "meaning": "Value creation and sustainable monetization"}
                ]
            }
            os.makedirs(os.path.dirname(lexicon_json_path), exist_ok=True)
            with open(lexicon_json_path, 'w', encoding='utf-8') as f:
                json.dump(default_data, f, ensure_ascii=False, indent=2)
                
        with open(lexicon_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        terms = data.get('terms', [])
        
        os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
        with open(output_csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['term', 'category', 'meaning'])
            for item in terms:
                writer.writerow([
                    item.get('term', ''),
                    item.get('category', ''),
                    item.get('meaning', '')
                ])
                
        print(f"Successfully exported lexicon to {output_csv_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
