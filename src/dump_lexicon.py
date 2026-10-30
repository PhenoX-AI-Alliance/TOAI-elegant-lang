import sys
import os
import json

def dump_lexicon():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    if not os.path.exists(lexicon_path):
        print("Lexicon file not found:", lexicon_path)
        sys.exit(1)
    with open(lexicon_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print("# TOAI Core Lexicon Table")
    print("")
    print(f"Version: {data.get('version', 'N/A')}")
    print("")
    print("| Term | Category | Definition |")
    print("|---|---|---|")
    for entry in data.get("entries", []):
        print(f"| {entry.get('term', '')} | {entry.get('category', '')} | {entry.get('definition', '')} |")

if __name__ == "__main__":
    dump_lexicon()
