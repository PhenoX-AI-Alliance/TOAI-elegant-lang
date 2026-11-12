import sys
import os
import traceback
import time
import json
import csv

def main():
    try:
        project_dir = '/home/phenox/gemini-sandbox/TOAI-elegant-lang'
        core_lexicon_path = os.path.join(project_dir, 'core_lexicon.json')
        output_csv_path = os.path.join(project_dir, 'lexicon_export.csv')
        
        if not os.path.exists(core_lexicon_path):
            sample_data = {
                "version": "1.0.0",
                "lexicon": [
                    {"id": 1, "term": "TOAI", "category": "Core", "description": "Tree of Artificial Intelligence"},
                    {"id": 2, "term": "Elegant", "category": "Style", "description": "Clean and robust implementation"}
                ]
            }
            os.makedirs(os.path.dirname(core_lexicon_path), exist_ok=True)
            with open(core_lexicon_path, 'w', encoding='utf-8') as f:
                json.dump(sample_data, f, indent=2, ensure_ascii=False)
        
        with open(core_lexicon_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        lexicon_items = data.get('lexicon', [])
        
        with open(output_csv_path, 'w', encoding='utf-8', newline='') as csvfile:
            fieldnames = ['id', 'term', 'category', 'description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item in lexicon_items:
                writer.writerow({
                    'id': item.get('id', ''),
                    'term': item.get('term', ''),
                    'category': item.get('category', ''),
                    'description': item.get('description', '')
                })
                
        print(f"Successfully exported lexicon to {{output_csv_path}}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
