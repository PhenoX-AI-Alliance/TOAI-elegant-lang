import sys
import os
import traceback
import time
import json
import csv

def main():
    base_dir = '/home/phenox/gemini-sandbox/TOAI-elegant-lang'
    json_path = os.path.join(base_dir, 'core_lexicon.json')
    csv_path = os.path.join(base_dir, 'core_lexicon.csv')
    
    if not os.path.exists(json_path):
        default_data = {
            "version": "1.0.0",
            "description": "Core lexicon for TOAI elegant language",
            "entries": [
                {"term": "Gaia", "category": "ecosystem", "meaning": "Earth of Life, core ecosystem concept."},
                {"term": "Altruism", "category": "philosophy", "meaning": "Selfless concern for the well-being of others."}
            ]
        }
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)
            
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    entries = data.get('entries', [])
    
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['term', 'category', 'meaning'])
        for entry in entries:
            writer.writerow([
                entry.get('term', ''),
                entry.get('category', ''),
                entry.get('meaning', '')
            ])
            
    print(f"Successfully exported lexicon to {csv_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
