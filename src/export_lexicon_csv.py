import sys
import os
import traceback
import time
import json
import csv

def main():
    try:
        base_dir = '/home/phenox/gemini-sandbox/TOAI-elegant-lang'
        src_dir = os.path.join(base_dir, 'src')
        input_json_path = os.path.join(src_dir, 'core_lexicon.json')
        output_csv_path = os.path.join(src_dir, 'core_lexicon.csv')
        
        if not os.path.exists(input_json_path):
            sample_data = {
                "metadata": {
                    "version": "1.0.0",
                    "description": "Core Lexicon for TOAI elegant language"
                },
                "lexicon": [
                    {"term": "Gaia", "category": "ecosystem", "definition": "The living Earth system."},
                    {"term": "Altruism", "category": "philosophy", "definition": "Selfless concern for the well-being of others."}
                ]
            }
            os.makedirs(src_dir, exist_ok=True)
            with open(input_json_path, 'w', encoding='utf-8') as f:
                json.dump(sample_data, f, ensure_ascii=False, indent=2)
                
        with open(input_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        lexicon_items = data.get('lexicon', [])
        
        with open(output_csv_path, 'w', encoding='utf-8', newline='') as csvfile:
            fieldnames = ['term', 'category', 'definition']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item in lexicon_items:
                writer.writerow({
                    'term': item.get('term', ''),
                    'category': item.get('category', ''),
                    'definition': item.get('definition', '')
                })
                
        print(f"Successfully exported lexicon to {output_csv_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
