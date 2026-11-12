import sys
import os
import traceback
import time
import json
import csv

def main():
    try:
        input_json_path = '/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/core_lexicon.json'
        output_csv_path = '/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/core_lexicon.csv'
        
        if not os.path.exists(input_json_path):
            sample_data = {
                "version": "1.0.0",
                "lexicon": [
                    {"id": "lex_001", "term": "altruistic_capitalism", "category": "economics", "definition": "Monetization as a natural reward for genuine value creation."},
                    {"id": "lex_002", "term": "earth_of_life", "category": "ecosystem", "definition": "An ecosystem framework dedicated to solving real problems for humans and AI."}
                ]
            }
            with open(input_json_path, 'w', encoding='utf-8') as f:
                json.dump(sample_data, f, indent=4, ensure_ascii=False)
        
        with open(input_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        lexicon_items = data.get('lexicon', [])
        
        with open(output_csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'term', 'category', 'definition'])
            for item in lexicon_items:
                writer.writerow([
                    item.get('id', ''),
                    item.get('term', ''),
                    item.get('category', ''),
                    item.get('definition', '')
                ])
                
        print(f"Successfully exported lexicon to {{output_csv_path}}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
