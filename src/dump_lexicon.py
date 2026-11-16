import sys
import os
import traceback
import time
import json

def dump_lexicon():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
        sys.exit(1)
        
    with open(lexicon_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    print("# TOAI Core Lexicon Table\n")
    print("| Term | Definition | Category |")
    print("|---|---|---|")
    
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                definition = str(value.get("definition", "N/A"))
                category = str(value.get("category", "N/A"))
            else:
                definition = str(value)
                category = "N/A"
            print(f"| {key} | {definition} | {category} |")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                term = str(item.get("term", item.get("name", "N/A")))
                definition = str(item.get("definition", "N/A"))
                category = str(item.get("category", "N/A"))
                print(f"| {term} | {definition} | {category} |")
            else:
                print(f"| {str(item)} | N/A | N/A |")

if __name__ == "__main__":
    try:
        dump_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
