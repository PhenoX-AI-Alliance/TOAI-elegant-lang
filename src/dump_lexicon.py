import sys
import os
import json

def dump_lexicon():
    lexicon_path = os.path.join(os.path.dirname(__file__), "lexicon", "core_lexicon.json")
    if not os.path.exists(lexicon_path):
        print(f"Error: {lexicon_path} not found.", file=sys.stderr)
        sys.exit(1)
        
    with open(lexicon_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    print("# TOAI Elegant Lang - Core Lexicon Table\n")
    print(f"**Version:** {data.get(\"version\", \"Unknown\")}")
    print(f"**Ecosystem:** {data.get(\"ecosystem\", \"Unknown\")}\n")
    print("| Term | Meaning | Category |")
    print("| :--- | :--- | :--- |")
    
    for item in data.get("lexicon", []):
        term = item.get("term", "")
        meaning = item.get("meaning", "")
        category = item.get("category", "")
        print(f"| {term} | {meaning} | {category} |")

if __name__ == "__main__":
    dump_lexicon()
