import sys
import os
import traceback
import json

def main():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
        sys.exit(1)
        
    items = []
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        if "lexicon" in data and isinstance(data["lexicon"], list):
            items = data["lexicon"]
        elif "words" in data and isinstance(data["words"], list):
            items = data["words"]
        else:
            items = [data]
    else:
        print("Error: Lexicon JSON root must be a list or a dictionary.", file=sys.stderr)
        sys.exit(1)
        
    print("# Core Lexicon Summary\n")
    print("| Term / ID | Category / Type | Description / Definition |")
    print("|---|---|---|")
    
    for item in items:
        if not isinstance(item, dict):
            continue
        term = str(item.get("term", item.get("id", item.get("name", "N/A"))))
        category = str(item.get("category", item.get("type", "N/A")))
        desc = str(item.get("description", item.get("definition", item.get("meaning", ""))))
        term = term.replace("|", "\\|")
        category = category.replace("|", "\\|")
        desc = desc.replace("|", "\\|").replace("\n", " ")
        print(f"| {term} | {category} | {desc} |")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
