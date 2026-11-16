import json
import csv
import os

def process_lexicon(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if data:
        keys = data[0].keys() if isinstance(data, list) else data.keys()
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data if isinstance(data, list) else [data])

if __name__ == "__main__":
    process_lexicon("/home/phenox/gemini-sandbox/TOAI_Generated/core_lexicon.json", "/home/phenox/gemini-sandbox/TOAI_Generated/lexicon_export.csv")
