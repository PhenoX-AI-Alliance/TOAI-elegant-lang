import sys
import os
import traceback
import time
import json
import csv

def main():
    try:
        base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        src_dir = os.path.join(base_dir, "src")
        data_dir = os.path.join(base_dir, "data")
        output_dir = os.path.join(base_dir, "output")
        
        os.makedirs(output_dir, exist_ok=True)
        
        json_path = os.path.join(data_dir, "core_lexicon.json")
        csv_path = os.path.join(output_dir, "core_lexicon.csv")
        
        if not os.path.exists(json_path):
            os.makedirs(data_dir, exist_ok=True)
            dummy_data = {
                "version": "1.0.0",
                "lexicon": [
                    {"id": "gaia_001", "term": "Gaia Ecosystem", "category": "Core", "description": "Earth of life and altruistic intelligence."},
                    {"id": "gaia_002", "term": "Altruistic Monetization", "category": "Economy", "description": "Sustainable value creation and rewards."}
                ]
            }
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(dummy_data, f, ensure_ascii=False, indent=2)
                
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        lexicon_items = []
        if isinstance(data, dict):
            if "lexicon" in data and isinstance(data["lexicon"], list):
                lexicon_items = data["lexicon"]
            else:
                lexicon_items = [data]
        elif isinstance(data, list):
            lexicon_items = data
            
        fieldnames = set()
        for item in lexicon_items:
            if isinstance(item, dict):
                fieldnames.update(item.keys())
        
        fieldnames_list = sorted(list(fieldnames))
        if not fieldnames_list:
            fieldnames_list = ["id", "term", "category", "description"]
            
        with open(csv_path, "w", encoding="utf-8", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames_list)
            writer.writeheader()
            for item in lexicon_items:
                if isinstance(item, dict):
                    filtered_item = {k: item.get(k, "") for k in fieldnames_list}
                    writer.writerow(filtered_item)
                    
        print(f"Successfully exported lexicon to {{csv_path}}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
