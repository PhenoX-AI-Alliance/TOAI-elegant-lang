import sys
import os
import json
import traceback

def dump_lexicon():
    try:
        lexicon_path = '/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json'
        if not os.path.exists(lexicon_path):
            print(f'Error: Lexicon file not found at {lexicon_path}', file=sys.stderr)
            sys.exit(1)
        
        with open(lexicon_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print('# TOAI Elegant Lang - Core Lexicon')
        print()
        print('| Term | Definition | Category |')
        print('|---|---|---|')
        
        items = data if isinstance(data, list) else data.get('lexicon', [])
        for item in items:
            term = item.get('term', '')
            definition = item.get('definition', '')
            category = item.get('category', '')
            print(f'| {term} | {definition} | {category} |')
            
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    dump_lexicon()
