import sys
import os
import traceback
import time
import json
import csv

def main():
    target_dir = '/home/phenox/gemini-sandbox/TOAI-elegant-lang/src'
    json_path = os.path.join(target_dir, 'core_lexicon.json')
    csv_path = os.path.join(target_dir, 'core_lexicon.csv')
    
    try:
        if not os.path.exists(json_path):
            print(f"Error: {json_path} does not exist. Creating default core_lexicon.json.")
            default_data = {
                "version": "1.0.0",
                "lexicon": [
                    {"term": "Gaia", "category": "ecosystem", "description": "The living Earth system."},
                    {"term": "AltruisticMonetization", "category": "economy", "description": "Generating value and revenue through genuine good."}
                ]
            }
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(default_data, f, ensure_ascii=False, indent=2)
                
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        lexicon_items = data.get('lexicon', [])
        
        with open(csv_path, 'w', encoding='utf-8', newline='') as csvfile:
            fieldnames = ['term', 'category', 'description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item in lexicon_items:
                writer.writerow({
                    'term': item.get('term', ''),
                    'category': item.get('category', ''),
                    'description': item.get('description', '')
                })
                
        print(f"Successfully exported {len(lexicon_items)} items to {csv_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
