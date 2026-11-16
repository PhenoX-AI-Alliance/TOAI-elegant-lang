# -*- coding: utf-8 -*-
import sys
import os
import json

def load_and_dump():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    if not os.path.exists(lexicon_path):
        print(f"Lexicon not found at {lexicon_path}")
        sys.exit(1)
        
    with open(lexicon_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    print("# TOAI Core Lexicon")
    print()
    print("| Term | Definition | Category | Usage |")
    print("|---|---|---|---|")
    
    for term, value in data.items():
        if isinstance(value, dict):
            defn = str(value.get("definition", "N/A"))
            cat = str(value.get("category", "general"))
            usage = str(value.get("usage", "N/A"))
        else:
            defn = str(value)
            cat = "general"
            usage = "N/A"
        print(f"| {term} | {defn} | {cat} | `{usage}` |")

if __name__ == "__main__":
    load_and_dump()
