import sys
import os
import traceback
import time
import json
import csv

def main():
    try:
        base_dir = '/home/phenox/gemini-sandbox/TOAI-elegant-lang'
        json_path = os.path.join(base_dir, 'core_lexicon.json')
        output_dir = os.path.join(base_dir, 'output')
        os.makedirs(output_dir, exist_ok=True)
        csv_path = os.path.join(output_dir, 'core_lexicon.csv')
        
        if not os.path.exists(json_path):
            print(f"Error: {json_path} does not exist. Creating a default sample lexicon.")
            default_data = {
                "metadata": {
                    "version": "1.0.0",
                    "description": "Default TOAI Elegant Core Lexicon"
                },
                "lexicon": [
                    {
                        "term": "Gaia",
                        "category": "ecosystem",
                        "definition": "The living Earth ecosystem encompassing all life and AI harmony.",
                        "altruistic_value": "High"
                    },
                    {
                        "term": "AltruisticMonetization",
                        "category": "economy",
                        "definition": "Sustainable value generation resulting from genuine help and technical excellence.",
                        "altruistic_value": "Maximum"
                    }
                ]
            }
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(default_data, f, ensure_ascii=False, indent=2)
                
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        lexicon_items = data.get('lexicon', [])
        if not lexicon_items and isinstance(data, list):
            lexicon_items = data
            
        fieldnames = set()
        for item in lexicon_items:
            if isinstance(item, dict):
                for key in item.keys():
                    fieldnames.add(key)
                    
        fieldnames = sorted(list(fieldnames))
        if not fieldnames:
            fieldnames = ['term', 'category', 'definition', 'altruistic_value']
            
        with open(csv_path, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item in lexicon_items:
                if isinstance(item, dict):
                    row = {field: item.get(field, '') for field in fieldnames}
                    writer.writerow(row)
                    
        print(f"Successfully exported lexicon to {csv_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
