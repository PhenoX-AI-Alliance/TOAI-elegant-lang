import sys
import os
import traceback
import time
import json
import csv

def convert_json_to_csv():
    base_dir = '/home/phenox/gemini-sandbox/TOAI-elegant-lang/src'
    json_path = os.path.join(base_dir, 'core_lexicon.json')
    csv_path = os.path.join(base_dir, 'core_lexicon.csv')

    if not os.path.exists(json_path):
        print(f"Error: {json_path} does not exist.")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    lexicon_items = data.get('lexicon', [])
    if not lexicon_items:
        print("Warning: No lexicon items found in JSON.")

    fieldnames = ['term', 'type', 'description']

    with open(csv_path, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in lexicon_items:
            row = {
                'term': item.get('term', ''),
                'type': item.get('type', ''),
                'description': item.get('description', '')
            }
            writer.writerow(row)

    print(f"Successfully exported lexicon to {csv_path}")

if __name__ == '__main__':
    try:
        convert_json_to_csv()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
