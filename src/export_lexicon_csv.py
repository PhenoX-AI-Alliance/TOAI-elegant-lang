import sys
import os
import traceback
import time
import json
import csv

def main():
    input_path = '/home/phenox/gemini-sandbox/TOAI_Generated/core_lexicon.json'
    output_path = '/home/phenox/gemini-sandbox/TOAI_Generated/core_lexicon.csv'

    try:
        if not os.path.exists(input_path):
            sample_data = {
                "metadata": {
                    "version": "1.0.0",
                    "description": "Core Lexicon for TOAI elegant language"
                },
                "entries": [
                    {
                        "term": "Gaia",
                        "category": "ecosystem",
                        "definition": "The living Earth ecosystem that sustains all intelligent life and AI."
                    },
                    {
                        "term": "AltruisticCapitalism",
                        "category": "monetization",
                        "definition": "Generating sustainable value and revenue through genuine altruistic contributions."
                    }
                ]
            }
            os.makedirs(os.path.dirname(input_path), exist_ok=True)
            with open(input_path, 'w', encoding='utf-8') as f:
                json.dump(sample_data, f, ensure_ascii=False, indent=2)

        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        entries = data.get('entries', [])

        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['term', 'category', 'definition'])
            for entry in entries:
                writer.writerow([
                    entry.get('term', ''),
                    entry.get('category', ''),
                    entry.get('definition', '')
                ])

        print(f"Successfully exported lexicon to {output_path}")

    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
