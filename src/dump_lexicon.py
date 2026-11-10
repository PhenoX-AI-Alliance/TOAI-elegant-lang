import sys
import os
import json
import traceback

def main():
    try:
        lexicon_path = '/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json'
        if not os.path.exists(lexicon_path):
            print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
            sys.exit(1)
            
        with open(lexicon_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        print("# TOAI Core Lexicon Dump")
        print("")
        print("| Term | Definition / Description |")
        print("|:--- |:--- |")
        
        if isinstance(data, dict):
            for key, value in data.items():
                print(f"| {key} | {value} |")
        elif isinstance(data, list):
            for item in data:
                term = item.get('term', 'N/A')
                desc = item.get('description', 'N/A')
                print(f"| {term} | {desc} |")
                
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
