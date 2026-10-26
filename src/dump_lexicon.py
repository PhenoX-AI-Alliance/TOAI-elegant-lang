import sys
import os
import json

def dump():
    lexicon_path = '/home/phenox/gemini-sandbox/lexicon/core_lexicon.json'
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {lexicon_path}")
        sys.exit(1)
        
    with open(lexicon_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    print("# Core Lexicon List\n")
    print(f"Version: {data.get('version', 'Unknown')}")
    print(f"Ecosystem: {data.get('ecosystem', 'Unknown')}\n")
    print("| Term | Definition |")
    print("| --- | --- |")
    
    for item in data.get('vocabulary', []):
        print(f"| {item.get('term', '')} | {item.get('definition', '')} |")

if __name__ == '__main__':
    dump()
