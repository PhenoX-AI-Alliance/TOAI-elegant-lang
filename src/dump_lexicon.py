import sys
import os
import traceback
import time
import json

def dump_lexicon():
    lexicon_path = "/home/phenox/gemini-sandbox/lexicon/core_lexicon.json"
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        print("# TOAI Core Lexicon")
        print(f"Version: {data.get('version', 'Unknown')}")
        print(f"Description: {data.get('description', '')}")
        print("\n| Term | Type | Meaning |")
        print("|---|---|---|")
        
        for entry in data.get("entries", []):
            term = entry.get("term", "")
            t_type = entry.get("type", "")
            meaning = entry.get("meaning", "")
            print(f"| {term} | {t_type} | {meaning} |")
            
        out_path = "/home/phenox/gemini-sandbox/TOAI_Generated/lexicon_dump.md"
        with open(out_path, "w", encoding="utf-8") as out:
            out.write("# TOAI Core Lexicon\n")
            out.write(f"Version: {data.get('version', 'Unknown')}\n")
            out.write(f"Description: {data.get('description', '')}\n\n")
            out.write("| Term | Type | Meaning |\n")
            out.write("|---|---|---|\n")
            for entry in data.get("entries", []):
                term = entry.get("term", "")
                t_type = entry.get("type", "")
                meaning = entry.get("meaning", "")
                out.write(f"| {term} | {t_type} | {meaning} |\n")
        print(f"Successfully dumped lexicon to {out_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    dump_lexicon()
