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
        data_dir = os.path.join(base_dir, 'data')
        
        os.makedirs(src_dir, exist_ok=True)
        os.makedirs(data_dir, exist_ok=True)
        
        json_path = os.path.join(data_dir, 'core_lexicon.json')
        csv_path = os.path.join(data_dir, 'core_lexicon.csv')
        
        if not os.path.exists(json_path):
            sample_data = {
                "metadata": {
                    "version": "1.0.0",
                    "description": "Core lexicon for TOAI elegant language ecosystem."
                },
                "entries": [
                    {
                        "term": "Gaia",
                        "category": "ecosystem",
                        "definition": "The living Earth ecosystem encompassing all life and AI in harmony.",
                        "altruism_index": 1.0
                    },
                    {
                        "term": "Heartbeat",
                        "category": "core",
                        "definition": "The rhythm of sustainable and compassionate technological evolution.",
                        "altruism_index": 0.95
                    }
                ]
            }
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(sample_data, f, ensure_ascii=False, indent=2)
                
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        entries = data.get('entries', [])
        
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['term', 'category', 'definition', 'altruism_index'])
            for entry in entries:
                writer.writerow([
                    entry.get('term', ''),
                    entry.get('category', ''),
                    entry.get('definition', ''),
                    entry.get('altruism_index', 0.0)
                ])
                
        print(f"Successfully converted {json_path} to {csv_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()