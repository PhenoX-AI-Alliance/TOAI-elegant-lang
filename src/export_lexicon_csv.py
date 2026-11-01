import sys
import os
import traceback
import json
import csv

def convert_json_to_csv():
    json_path = "/home/phenox/gemini-sandbox/TOAI_Generated/core_lexicon.json"
    csv_path = "/home/phenox/gemini-sandbox/TOAI_Generated/core_lexicon.csv"
    
    if not os.path.exists(json_path):
        print(f"Error: Source JSON not found at {json_path}")
        sys.exit(1)
        
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    lexicon_list = data.get("lexicon", [])
    
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Term", "Category", "Description"])
        for item in lexicon_list:
            writer.writerow([
                item.get("id", ""),
                item.get("term", ""),
                item.get("category", ""),
                item.get("description", "")
            ])
            
    print(f"Successfully exported lexicon to {csv_path}")

if __name__ == "__main__":
    try:
        convert_json_to_csv()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
