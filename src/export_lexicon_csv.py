import sys
import os
import traceback
import time
import json
import csv

def main():
    try:
        base_dir = '/home/phenox/gemini-sandbox/TOAI-elegant-lang'
        data_dir = os.path.join(base_dir, 'data')
        src_dir = os.path.join(base_dir, 'src')
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(src_dir, exist_ok=True)
        
        json_path = os.path.join(data_dir, 'core_lexicon.json')
        csv_path = os.path.join(data_dir, 'core_lexicon.csv')
        
        if not os.path.exists(json_path):
            sample_data = {
                "version": "1.0.0",
                "lexicon": [
                    {"term": "Gaia", "category": "ecosystem", "description": "The living Earth ecosystem."},
                    {"term": "AltruisticMonetization", "category": "economy", "description": "Generating value through kindness and sharing."}
                ]
            }
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(sample_data, f, ensure_ascii=False, indent=2)
                
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        lexicon_list = data.get('lexicon', [])
        
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['term', 'category', 'description'])
            for item in lexicon_list:
                writer.writerow([
                    item.get('term', ''),
                    item.get('category', ''),
                    item.get('description', '')
                ])
        
        print(f"Successfully exported lexicon to {{csv_path}}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()