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
            print(f"Error: {json_path} does not exist. Creating default sample data.")
            sample_data = {
                "metadata": {
                    "version": "1.0.0",
                    "description": "Core Lexicon for TOAI elegant lang"
                },
                "lexicon": [
                    {"term": "Gaia", "category": "ecosystem", "definition": "Earth of Life, core heartbeat."},
                    {"term": "Altruism", "category": "philosophy", "definition": "Selfless concern for the well-being of others."}
                ]
            }
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(sample_data, f, ensure_ascii=False, indent=2)
                
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        lexicon_items = data.get('lexicon', [])
        if not lexicon_items and isinstance(data, list):
            lexicon_items = data
        elif not lexicon_items and isinstance(data, dict):
            # Try to flatten if nested differently
            lexicon_items = [{"key": k, "value": str(v)} for k, v in data.items() if k != "metadata"]
            
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            if lexicon_items and isinstance(lexicon_items[0], dict):
                fieldnames = list(lexicon_items[0].keys())
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for item in lexicon_items:
                    writer.writerow(item)
            else:
                writer = csv.writer(csvfile)
                writer.writerow(["term"])
                for item in lexicon_items:
                    writer.writerow([str(item)])
                    
        print(f"Successfully exported lexicon to {csv_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
