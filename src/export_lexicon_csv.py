import sys
import os
import traceback
import time
import json
import csv

def main():
    try:
        repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        json_path = os.path.join(repo_dir, "lexicon", "core_lexicon.json")
        output_csv_path = os.path.join(repo_dir, "data", "core_lexicon.csv")
        
        os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
        
        if not os.path.exists(json_path):
            print(f"Error: {json_path} does not exist.")
            sys.exit(1)
            
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        if isinstance(data, dict):
            rows = []
            for k, v in data.items():
                if isinstance(v, dict):
                    row = {"key": k}
                    row.update(v)
                    rows.append(row)
                else:
                    rows.append({"key": k, "value": v})
        elif isinstance(data, list):
            rows = data
        else:
            print("Error: Unsupported JSON structure for CSV export.")
            sys.exit(1)
            
        if not rows:
            print("Warning: No data found to export.")
            fieldnames = ["key"]
        else:
            fieldnames = list(rows[0].keys())
            
        with open(output_csv_path, "w", encoding="utf-8", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
                
        print(f"Successfully exported lexicon to {output_csv_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
