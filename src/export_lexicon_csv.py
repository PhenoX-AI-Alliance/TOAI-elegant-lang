import sys
import os
import traceback
import time
import json
import csv

def export_lexicon():
    base_dir = '/home/phenox/gemini-sandbox/TOAI-elegant-lang'
    src_dir = os.path.join(base_dir, 'src')
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    json_path = os.path.join(src_dir, 'core_lexicon.json')
    csv_path = os.path.join(data_dir, 'core_lexicon.csv')
    
    if not os.path.exists(json_path):
        default_data = {
            "metadata": {
                "version": "1.0.0",
                "description": "Core lexicon for TOAI elegant language"
            },
            "lexicon": [
                {"term": "Gaia", "category": "ecosystem", "meaning": "Earth of Life, core ecosystem concept"},
                {"term": "Altruism", "category": "philosophy", "meaning": "Selfless concern for the well-being of others"},
                {"term": "Heartbeat", "category": "core", "meaning": "Pulse of the system and living entities"}
            ]
        }
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)
            
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    lexicon_list = data.get('lexicon', [])
    
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['term', 'category', 'meaning'])
        for item in lexicon_list:
            writer.writerow([
                item.get('term', ''),
                item.get('category', ''),
                item.get('meaning', '')
            ])
            
    print(f"Successfully exported lexicon to {csv_path}")

if __name__ == '__main__':
    try:
        export_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
