import sys
import os
import traceback
import time
import json

def dump_lexicon():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    if not os.path.exists(lexicon_path):
        print(f"Error: {lexicon_path} does not exist.", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}", file=sys.stderr)
        sys.exit(1)
        
    print("# TOAI Core Lexicon")
    print("")
    version = data.get("version", "Unknown")
    print(f"Version: {version}")
    print("")
    print("| Term | Category | Description |")
    print("|---|---|---|")
    
    items = data.get("lexicon", [])
    for item in items:
        term = item.get("term", "")
        category = item.get("category", "")
        desc = item.get("description", "")
        print(f"| {term} | {category} | {desc} |")

if __name__ == "__main__":
    try:
        dump_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
