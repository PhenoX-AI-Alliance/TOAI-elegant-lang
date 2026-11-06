# -*- coding: utf-8 -*-
import sys
import os
import json
import traceback

def main():
    lexicon_path = '/home/phenox/gemini-sandbox/lexicon/core_lexicon.json'
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(lexicon_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}", file=sys.stderr)
        sys.exit(1)
        
    print("# TOAI Core Lexicon Reference")
    print("")
    print("Generated automatically by dump_lexicon.py")
    print("")
    print("| Term / Key | Definition / Value |")
    print("|---|---|")
    
    if isinstance(data, dict):
        for k, v in data.items():
            print(f"| `{k}` | {str(v).replace(chr(124), '&#124;')} |")
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            print(f"| [{idx}] | {str(item).replace(chr(124), '&#124;')} |")
    else:
        print(f"| Data | {str(data).replace(chr(124), '&#124;')} |")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
