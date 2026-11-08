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
                    "description": "Core lexicon for TOAI elegant language"
                },
                "entries": [
                    {
                        "term": "gaia_ecosystem",
                        "category": "philosophy",
                        "definition": "The living network of altruism, warmth, and technological harmony."
                    },
                    {
                        "term": "altruistic_monetization",
                        "category": "economics",
                        "definition": "The natural reward of sustainable value creation and sharing."
                    }
                ]
            }
            os.makedirs(src_dir, exist_ok=True)
            with open(input_json_path, 'w', encoding='utf-8') as f:
                json.dump(sample_data, f, ensure_ascii=False, indent=2)
                
        with open(input_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        entries = data.get('entries', [])
        if not entries and isinstance(data, dict):
            entries = [data]
        elif not isinstance(entries, list):
            entries = [{"value": str(data)}]
            
        with open(output_csv_path, 'w', encoding='utf-8', newline='') as csvfile:
            fieldnames = set()
            for entry in entries:
                if isinstance(entry, dict):
                    fieldnames.update(entry.keys())
            
            if not fieldnames:
                fieldnames = {'term', 'category', 'definition'}
                
            fieldnames_list = sorted(list(fieldnames))
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames_list)
            
            writer.writeheader()
            for entry in entries:
                if isinstance(entry, dict):
                    row = {k: entry.get(k, '') for k in fieldnames_list}
                    writer.writerow(row)
                else:
                    writer.writerow({fieldnames_list[0]: str(entry)})
                    
        print(f"Successfully exported lexicon CSV to {output_csv_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
