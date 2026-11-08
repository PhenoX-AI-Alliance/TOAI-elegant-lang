import sys
import os
import traceback
import time
import json
import csv

def main():
    try:
        sandbox_dir = '/home/phenox/gemini-sandbox'
        lexicon_json_path = os.path.join(sandbox_dir, 'TOAI-elegant-lang', 'src', 'core_lexicon.json')
        output_csv_path = os.path.join(sandbox_dir, 'TOAI-elegant-lang', 'src', 'core_lexicon.csv')
        
        if not os.path.exists(lexicon_json_path):
            default_data = {
                "version": "1.0.0",
                "description": "Core lexicon for TOAI elegant language ecosystem",
                "terms": [
                    {"id": 1, "term": "Gaia", "category": "ecosystem", "definition": "The living Earth ecosystem."},
                    {"id": 2, "term": "Altruism", "category": "philosophy", "definition": "Selfless concern for the well-being of others."}
                ]
            }
            os.makedirs(os.path.dirname(lexicon_json_path), exist_ok=True)
            with open(lexicon_json_path, 'w', encoding='utf-8') as f:
                json.dump(default_data, f, ensure_ascii=False, indent=2)
                
        with open(lexicon_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        terms = data.get('terms', [])
        
        with open(output_csv_path, 'w', encoding='utf-8', newline='') as csvfile:
            fieldnames = ['id', 'term', 'category', 'definition']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item in terms:
                writer.writerow({
                    'id': item.get('id', ''),
                    'term': item.get('term', ''),
                    'category': item.get('category', ''),
                    'definition': item.get('definition', '')
                })
                
        print(f"Successfully exported lexicon to {{output_csv_path}}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
