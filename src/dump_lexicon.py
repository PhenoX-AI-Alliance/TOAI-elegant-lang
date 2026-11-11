# -*- coding: utf-8 -*-
import sys
import os
import json

def dump_lexicon():
    base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
    lexicon_path = os.path.join(base_dir, "lexicon", "core_lexicon.json")
    
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
        sys.exit(1)
        
    print("# TOAI-elegant-lang Core Lexicon")
    print("")
    print(f"Version: {data.get('version', 'Unknown')}")
    print("")
    print("| Term | Type | Definition |")
    print("|---|---|---|")
    
    for item in data.get("lexicon", []):
        term = item.get("term", "")
        t_type = item.get("type", "")
        definition = item.get("definition", "")
        print(f"| {term} | {t_type} | {definition} |")

if __name__ == "__main__":
    dump_lexicon()
