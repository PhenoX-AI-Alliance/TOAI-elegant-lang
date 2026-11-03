import sys
import os
import traceback
import time
import json
import csv

def main():
    json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/core_lexicon.json"))
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/core_lexicon.csv"))
    
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    
    if not os.path.exists(json_path):
        sample_data = [
            {"id": "gaia_001", "term": "Gaia", "definition": "The living Earth ecosystem integrating all life and environments."},
            {"id": "gaia_002", "term": "Altruistic Monetization", "definition": "Monetization achieved as a natural reward for creating genuine value."}
        ]
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(sample_data, f, ensure_ascii=False, indent=2)
            
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    if isinstance(data, dict):
        lexicon_items = data.get("lexicon", [])
    elif isinstance(data, list):
        lexicon_items = data
    else:
        lexicon_items = []
        
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "term", "definition"])
        for item in lexicon_items:
            if isinstance(item, dict):
                writer.writerow([
                    item.get("id", ""),
                    item.get("term", ""),
                    item.get("definition", "")
                ])
                
    print(f"Successfully exported lexicon to {{csv_path}}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
