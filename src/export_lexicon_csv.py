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
            print(f"Error: {json_path} does not exist.")
            sys.exit(1)

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if isinstance(data, dict):
            rows = []
            for key, value in data.items():
                if isinstance(value, dict):
                    row = {'key': key}
                    row.update(value)
                    rows.append(row)
                else:
                    rows.append({'key': key, 'value': value})
        elif isinstance(data, list):
            rows = data
        else:
            print("Error: Unsupported JSON structure.")
            sys.exit(1)

        if not rows:
            print("Warning: No data to export.")
            fieldnames = ['key']
        else:
            fieldnames = list(rows[0].keys())

        with open(csv_path, 'w', encoding='utf-8', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                filtered_row = {k: (str(v) if isinstance(v, (dict, list)) else v) for k, v in row.items()}
                writer.writerow(filtered_row)

        print(f"Successfully exported lexicon to {csv_path}")

    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
