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
                    "description": "Core Lexicon for TOAI-elegant-lang"
                },
                "lexicon": [
                    {
                        "term": "gaia",
                        "category": "ecosystem",
                        "definition": "The living earth ecosystem emphasizing altruism and warmth.",
                        "synonyms": ["earth", "biosphere"]
                    },
                    {
                        "term": "altruistic_monetization",
                        "category": "economics",
                        "definition": "The natural reward of sustainable value creation.",
                        "synonyms": ["conscious_capitalism", "value_sharing"]
                    }
                ]
            }
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(sample_data, f, indent=2, ensure_ascii=False)
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        lexicon_items = data.get('lexicon', [])
        
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['term', 'category', 'definition', 'synonyms'])
            for item in lexicon_items:
                term = item.get('term', '')
                category = item.get('category', '')
                definition = item.get('definition', '')
                synonyms = ','.join(item.get('synonyms', []))
                writer.writerow([term, category, definition, synonyms])
                
        print(f"Successfully converted {{json_path}} to {{csv_path}}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
