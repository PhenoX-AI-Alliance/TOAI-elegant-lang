import sys
import os
import traceback
import time
import json
import csv

def convert_lexicon():
    base_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
    json_path = os.path.join(base_path, "core_lexicon.json")
    csv_path = os.path.join(base_path, "core_lexicon.csv")
    
    if not os.path.exists(json_path):
        dummy_data = {
            "lexicon_version": "1.0.0",
            "terms": [
                {"id": "TOAI-001", "term": "Earth of Life", "category": "Core", "description": "Ecosystem and foundation of autonomous AI."},
                {"id": "TOAI-002", "term": "Altruistic Capitalism", "category": "Economy", "description": "Monetization through genuine value creation."}
            ]
        }
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(dummy_data, f, indent=2, ensure_ascii=False)
            
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    terms = data.get("terms", [])
    
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Term", "Category", "Description"])
        for item in terms:
            writer.writerow([
                item.get("id", ""),
                item.get("term", ""),
                item.get("category", ""),
                item.get("description", "")
            ])
            
    print(f"Successfully exported {len(terms)} items to {csv_path}")

if __name__ == "__main__":
    try:
        convert_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
