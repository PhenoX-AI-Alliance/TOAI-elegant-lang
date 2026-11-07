import sys
import os
import traceback
import json

def main():
    lexicon_path = '/home/phenox/gemini-sandbox/lexicon/core_lexicon.json'
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {{lexicon_path}}", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(lexicon_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {{e}}", file=sys.stderr)
        sys.exit(1)
        
    print("# TOAI Core Lexicon")
    print("")
    print("| Term | Description | Category |")
    print("| --- | --- | --- |")
    
    items = data if isinstance(data, list) else data.get('lexicon', [])
    for item in items:
        term = item.get('term', '')
        desc = item.get('description', '')
        cat = item.get('category', '')
        print(f"| {{term}} | {{desc}} | {{cat}} |")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
