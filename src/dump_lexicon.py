# -*- coding: utf-8 -*-
import sys
import os
import json
import traceback

def dump_lexicon():
    try:
        lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
        if not os.path.exists(lexicon_path):
            print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
            sys.exit(1)
            
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        print("# TOAI Core Lexicon\n")
        print("| Term | Definition |")
        print("|---|---|")
        
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    term = item.get("term", "")
                    definition = item.get("definition", "")
                    print(f"| {term} | {definition} |")
                elif isinstance(item, str):
                    print(f"| {item} | - |")
        elif isinstance(data, dict):
            for term, definition in data.items():
                print(f"| {term} | {definition} |")
                
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    dump_lexicon()
