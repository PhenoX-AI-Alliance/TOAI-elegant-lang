import sys
import os
import traceback
import time
import json
import csv

def main():
    input_json_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/core_lexicon.json"
    output_csv_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/core_lexicon.csv"
    
    if not os.path.exists(input_json_path):
        print(f"Error: {input_json_path} does not exist.")
        sys.exit(1)
        
    try:
        with open(input_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        if isinstance(data, dict):
            lexicon_items = data.get("lexicon", [])
        elif isinstance(data, list):
            lexicon_items = data
        else:
            lexicon_items = []
            
        with open(output_csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["term", "definition", "category", "tags"])
            
            for item in lexicon_items:
                if isinstance(item, dict):
                    term = item.get("term", "")
                    definition = item.get("definition", "")
                    category = item.get("category", "")
                    tags = ",".join(item.get("tags", [])) if isinstance(item.get("tags"), list) else str(item.get("tags", ""))
                    writer.writerow([term, definition, category, tags])
                    
        print(f"Successfully exported lexicon to {output_csv_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
