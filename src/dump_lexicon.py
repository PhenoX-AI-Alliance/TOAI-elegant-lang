#!/usr/bin/env python3
import sys
import os
import json

def dump():
    lexicon_path = "/home/phenox/gemini-sandbox/lexicon/core_lexicon.json"
    if not os.path.exists(lexicon_path):
        print(f"Error: {lexicon_path} not found.", file=sys.stderr)
        sys.exit(1)
    with open(lexicon_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print("# TOAI Core Lexicon")
    print("")
    print("| Term | Category | Definition |")
    print("|---|---|---|")
    items = data.get("lexicon", [])
    if isinstance(items, list):
        for item in items:
            t = item.get("term", "")
            c = item.get("category", "")
            d = item.get("definition", "")
            print(f"| {t} | {c} | {d} |")

if __name__ == "__main__":
    dump()
