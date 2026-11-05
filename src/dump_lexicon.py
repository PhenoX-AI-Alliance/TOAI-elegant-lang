# -*- coding: utf-8 -*-
import sys
import os
import json
import traceback

def main():
    lexicon_path = '/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json'
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(lexicon_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}", file=sys.stderr)
        sys.exit(1)
        
    print("# TOAI Core Lexicon Report")
    print("")
    if "version" in data:
        print(f"**Version:** {data['version']}")
    if "description" in data:
        print(f"**Description:** {data['description']}")
    print("")
    print("| Term | Category | Definition |")
    print("|---|---|---|")
    
    entries = data.get("entries", [])
    for entry in entries:
        term = entry.get("term", "")
        category = entry.get("category", "")
        definition = entry.get("definition", "")
        print(f"| {term} | {category} | {definition} |")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
