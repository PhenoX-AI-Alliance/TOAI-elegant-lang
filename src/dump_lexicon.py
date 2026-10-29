import sys
import os
import json

def dump_lexicon():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
        sys.exit(1)
        
    with open(lexicon_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    print("# TOAI Core Lexicon")
    print()
    print(f"Version: {data.get('version', 'unknown')}")
    print(f"Description: {data.get('description', '')}")
    print()
    print("| Word | Meaning | Category |")
    print("|---|---|---|")
    
    for item in data.get("terms", []):
        word = item.get("word", "")
        meaning = item.get("meaning", "")
        category = item.get("category", "")
        print(f"| {word} | {meaning} | {category} |")

if __name__ == "__main__":
    dump_lexicon()
