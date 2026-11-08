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
                "lexicon": [
                    {"id": "1", "term": "Gaia", "category": "ecosystem", "description": "The living Earth ecosystem."},
                    {"id": "2", "term": "Altruism", "category": "philosophy", "description": "Selfless concern for the well-being of others."}
                ]
            }
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(sample_data, f, ensure_ascii=False, indent=4)
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        items = data.get('lexicon', [])
        if not items and isinstance(data, list):
            items = data
        elif not items and isinstance(data, dict):
            items = [data]
            
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            if items and isinstance(items[0], dict):
                fieldnames = list(items[0].keys())
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for item in items:
                    writer.writerow(item)
            else:
                writer = csv.writer(f)
                writer.writerow(["data"])
                for item in items:
                    writer.writerow([str(item)])
                    
        print(f"Successfully exported lexicon to {csv_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
