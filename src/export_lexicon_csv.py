import sys
import os
import traceback
import time
import json
import csv

def export_lexicon():
    source_json = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/core_lexicon.json"
    output_csv = "/home/phenox/gemini-sandbox/TOAI_Generated/core_lexicon_export.csv"
    
    try:
        if not os.path.exists(source_json):
            print(f"Source JSON not found at {source_json}. Creating a sample lexicon.")
            sample_data = {
                "version": "1.0.0",
                "lexicon": [
                    {"term": "Gaia", "category": "ecosystem", "description": "The living Earth system."},
                    {"term": "AltruisticCapitalism", "category": "monetization", "description": "Value creation aligned with well-being."}
                ]
            }
            os.makedirs(os.path.dirname(source_json), exist_ok=True)
            with open(source_json, "w", encoding="utf-8") as f:
                json.dump(sample_data, f, ensure_ascii=False, indent=2)
        
        with open(source_json, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        entries = data.get("lexicon", [])
        if not entries and isinstance(data, list):
            entries = data
            
        with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["term", "category", "description"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for entry in entries:
                if isinstance(entry, dict):
                    writer.writerow({
                        "term": entry.get("term", ""),
                        "category": entry.get("category", ""),
                        "description": entry.get("description", "")
                    })
                    
        print(f"Successfully exported lexicon to {output_csv}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    export_lexicon()
