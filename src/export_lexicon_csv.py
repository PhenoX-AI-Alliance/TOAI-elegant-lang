import sys
import os
import traceback
import time
import json
import csv

def export_csv():
    input_json_path = '/home/phenox/gemini-sandbox/TOAI_Generated/core_lexicon.json'
    output_csv_path = '/home/phenox/gemini-sandbox/TOAI_Generated/core_lexicon.csv'
    
    if not os.path.exists(input_json_path):
        sample_data = {
            "lexicon_version": "1.0.0",
            "terms": [
                {"id": 1, "term": "Gaia", "definition": "Earth ecosystem heartbeat"},
                {"id": 2, "term": "AltruisticMonetization", "definition": "Value creation and sustainable reward"}
            ]
        }
        os.makedirs(os.path.dirname(input_json_path), exist_ok=True)
        with open(input_json_path, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, ensure_ascii=False, indent=2)

    with open(input_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    terms = data.get('terms', [])
    
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'term', 'definition'])
        for item in terms:
            writer.writerow([item.get('id'), item.get('term'), item.get('definition')])
            
    print(f"Successfully exported {len(terms)} items to {output_csv_path}")

if __name__ == '__main__':
    try:
        export_csv()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
