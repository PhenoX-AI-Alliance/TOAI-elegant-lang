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
        data_dir = os.path.join(base_dir, 'data')
        
        os.makedirs(src_dir, exist_ok=True)
        os.makedirs(data_dir, exist_ok=True)
        
        json_path = os.path.join(data_dir, 'core_lexicon.json')
        csv_path = os.path.join(data_dir, 'core_lexicon.csv')
        
        if not os.path.exists(json_path):
            sample_data = {
                "version": "1.0.0",
                "lexicon": [
                    {"term": "toai_core", "type": "keyword", "description": "Core intelligence unit"},
                    {"term": "altruistic_capitalism", "type": "concept", "description": "Monetization through genuine value"}
                ]
            }
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(sample_data, f, ensure_ascii=False, indent=2)
                
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        lexicon_list = data.get('lexicon', [])
        
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['term', 'type', 'description'])
            for item in lexicon_list:
                writer.writerow([
                    item.get('term', ''),
                    item.get('type', ''),
                    item.get('description', '')
                ])
                
        print(f"Successfully exported lexicon to {{csv_path}}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
