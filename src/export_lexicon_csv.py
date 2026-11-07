import sys
import os
import traceback
import time
import json
import csv

def convert_json_to_csv():
    target_dir = '/home/phenox/gemini-sandbox/TOAI-elegant-lang/src'
    json_path = os.path.join(target_dir, 'core_lexicon.json')
    csv_path = os.path.join(target_dir, 'core_lexicon.csv')
    
    if not os.path.exists(json_path):
        print(f"Error: {json_path} does not exist. Creating a default sample.")
        default_data = {
            "version": "1.0.0",
            "terms": [
                {"id": 1, "term": "Gaia", "category": "ecosystem", "description": "The Earth ecosystem core."},
                {"id": 2, "term": "Altruism", "category": "philosophy", "description": "Selfless concern for the well-being of others."}
            ]
        }
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)
            
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        terms = data.get('terms', [])
        if not terms and isinstance(data, list):
            terms = data
            
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            if not terms:
                print("Warning: No terms found in JSON to export.")
                return
                
            sample_item = terms[0]
            if isinstance(sample_item, dict):
                fieldnames = list(sample_item.keys())
            else:
                fieldnames = ['value']
                
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for item in terms:
                if isinstance(item, dict):
                    writer.writerow(item)
                else:
                    writer.writerow({'value': item})
                    
        print(f"Successfully exported {json_path} to {csv_path}")
    except Exception as e:
        print(f"Failed to convert lexicon: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    try:
        convert_json_to_csv()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)