import sys
import os
import traceback
import time
import json
import csv

def main():
    sandbox_dir = '/home/phenox/gemini-sandbox'
    lexicon_json_path = os.path.join(sandbox_dir, 'TOAI-elegant-lang', 'core_lexicon.json')
    output_csv_path = os.path.join(sandbox_dir, 'TOAI-elegant-lang', 'src', 'lexicon_export.csv')
    
    try:
        if not os.path.exists(lexicon_json_path):
            print(f"Error: {lexicon_json_path} does not exist. Creating default core_lexicon.json.")
            os.makedirs(os.path.dirname(lexicon_json_path), exist_ok=True)
            default_data = {
                "version": "1.0.0",
                "lexicon": [
                    {"term": "Gaia", "category": "ecosystem", "description": "The living Earth ecosystem."},
                    {"term": "Altruism", "category": "philosophy", "description": "Selfless concern for the well-being of others."}
                ]
            }
            with open(lexicon_json_path, 'w', encoding='utf-8') as f:
                json.dump(default_data, f, indent=2, ensure_ascii=False)
                
        with open(lexicon_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        lexicon_items = data.get('lexicon', [])
        
        os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
        
        with open(output_csv_path, 'w', encoding='utf-8', newline='') as csvfile:
            fieldnames = ['term', 'category', 'description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for item in lexicon_items:
                writer.writerow({
                    'term': item.get('term', ''),
                    'category': item.get('category', ''),
                    'description': item.get('description', '')
                })
                
        print(f"Successfully exported lexicon to {output_csv_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
