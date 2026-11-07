import sys
import os
import traceback
import time
import json

def main():
    try:
        lexicon_path = "/home/phenox/gemini-sandbox/lexicon/core_lexicon.json"
        
        if not os.path.exists(lexicon_path):
            lexicon_dir = os.path.dirname(lexicon_path)
            os.makedirs(lexicon_dir, exist_ok=True)
            default_data = {
                "version": "1.0.0",
                "lexicon": [
                    {"term": "Gaia", "definition": "The living Earth ecosystem integrating all life and AI.", "category": "Core"},
                    {"term": "AltruisticMonetization", "definition": "Generating sustainable value through mutual aid and contribution.", "category": "Economy"}
                ]
            }
            with open(lexicon_path, "w", encoding="utf-8") as f:
                json.dump(default_data, f, indent=2, ensure_ascii=False)
                
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        print("# TOAI Core Lexicon")
        print()
        print(f"Version: {data.get('version', 'Unknown')}")
        print()
        print("| Term | Definition | Category |")
        print("| :--- | :--- | :--- |")
        
        for item in data.get("lexicon", []):
            term = item.get("term", "")
            definition = item.get("definition", "")
            category = item.get("category", "")
            print(f"| {term} | {definition} | {category} |")
            
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
