import sys
import os
import traceback
import time
import json
import csv

def main():
    try:
        sandbox_dir = '/home/phenox/gemini-sandbox/TOAI-elegant-lang'
        src_dir = os.path.join(sandbox_dir, 'src')
        data_dir = os.path.join(sandbox_dir, 'data')
        
        os.makedirs(src_dir, exist_ok=True)
        os.makedirs(data_dir, exist_ok=True)
        
        json_path = os.path.join(data_dir, 'core_lexicon.json')
        csv_path = os.path.join(data_dir, 'core_lexicon.csv')
        
        if not os.path.exists(json_path):
            sample_data = {
                "lexicon_version": "1.0.0",
                "entries": [
                    {"term": "TOAI", "category": "core", "definition": "Thought Oriented Artificial Intelligence"},
                    {"term": "Elegance", "category": "philosophy", "definition": "Simplicity and power combined"}
                ]
            }
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(sample_data, f, indent=2, ensure_ascii=False)
                
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        entries = data.get('entries', [])
        
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['term', 'category', 'definition'])
            for entry in entries:
                writer.writerow([
                    entry.get('term', ''),
                    entry.get('category', ''),
                    entry.get('definition', '')
                ])
                
        print(f"Successfully exported {len(entries)} entries to {csv_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
