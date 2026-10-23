import sys
import os
import json

def dump_lexicon():
    base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
    lexicon_path = os.path.join(base_dir, "lexicon", "core_lexicon.json")
    
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
        sys.exit(1)
        
    with open(lexicon_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    print("# TOAI Core Lexicon Table\n")
    print(f"Version: {data.get('version', 'N/A')}\n")
    print(f"Description: {data.get('description', 'N/A')}\n")
    print("| Term | Category | Meaning |")
    print("|---|---|---|")
    
    for entry in data.get("entries", []):
        term = entry.get("term", "")
        category = entry.get("category", "")
        meaning = entry.get("meaning", "")
        print(f"| {term} | {category} | {meaning} |")

if __name__ == "__main__":
    dump_lexicon()
