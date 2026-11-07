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
    
    if not os.path.exists(json_path):
        # Create a sample core_lexicon.json if it does not exist
        sample_data = [
            {"term": "Gaia", "category": "ecosystem", "definition": "The living Earth system."},
            {"term": "Altruism", "category": "philosophy", "definition": "Regard for others, both human and artificial."}
        ]
        os.makedirs(target_dir, exist_ok=True)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, ensure_ascii=False, indent=2)
            
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    if not isinstance(data, list) or len(data) == 0:
        raise ValueError("core_lexicon.json must contain a non-empty list of dictionaries.")
        
    fieldnames = list(data[0].keys())
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            if isinstance(item, dict):
                writer.writerow(item)
            else:
                raise TypeError("Each item in core_lexicon.json must be a dictionary.")
                
    print(f"Successfully exported {len(data)} items to {csv_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
