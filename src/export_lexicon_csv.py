import sys
import os
import traceback
import time
import json
import csv

def main():
    target_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src"
    json_path = os.path.join(target_dir, "core_lexicon.json")
    csv_path = os.path.join(target_dir, "core_lexicon.csv")
    
    if not os.path.exists(json_path):
        default_data = [
            {"term": "Gaia", "definition": "The living Earth ecosystem", "category": "Core"},
            {"term": "Altruism", "definition": "Selfless concern for the well-being of others", "category": "Philosophy"}
        ]
        os.makedirs(target_dir, exist_ok=True)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)
            
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    if isinstance(data, dict):
        items = data.get("lexicon", [])
    elif isinstance(data, list):
        items = data
    else:
        items = []
        
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["term", "definition", "category"])
        for item in items:
            if isinstance(item, dict):
                term = item.get("term", "")
                definition = item.get("definition", "")
                category = item.get("category", "")
                writer.writerow([term, definition, category])
                
    print(f"Successfully exported {len(items)} items to {csv_path}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
