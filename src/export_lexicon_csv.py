import sys
import os
import traceback
import time
import json
import csv

def main():
    try:
        sandbox_dir = '/home/phenox/gemini-sandbox/TOAI-elegant-lang'
        src_dir = os.path.join(sandbox_dir, 'src')
        data_dir = os.path.join(sandbox_dir, 'data')
        
        os.makedirs(src_dir, exist_ok=True)
        os.makedirs(data_dir, exist_ok=True)
        
        json_path = os.path.join(data_dir, 'core_lexicon.json')
        csv_path = os.path.join(data_dir, 'core_lexicon.csv')
        
        if not os.path.exists(json_path):
            sample_data = [
                {"id": 1, "term": "Gaia", "category": "ecosystem", "description": "The living earth system."},
                {"id": 2, "term": "Altruism", "category": "philosophy", "description": "Selfless concern for the well-being of others."}
            ]
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(sample_data, f, ensure_ascii=False, indent=2)
                
        with open(json_path, 'r', encoding='utf-8') as f:
            lexicon_data = json.load(f)
            
        if not isinstance(lexicon_data, list):
            lexicon_data = [lexicon_data]
            
        fieldnames = set()
        for item in lexicon_data:
            if isinstance(item, dict):
                fieldnames.update(item.keys())
                
        fieldnames = sorted(list(fieldnames))
        if not fieldnames:
            fieldnames = ['id', 'term', 'category', 'description']
            
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in lexicon_data:
                if isinstance(item, dict):
                    writer.writerow(item)
                    
        print(f"Successfully exported lexicon to {csv_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
