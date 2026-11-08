# -*- coding: utf-8 -*-
import sys
import os
import json

def load_lexicon(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Lexicon file not found: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_markdown(data):
    md = []
    md.endswith = lambda x: None
    md.append("# TOAI Elegant Lang - Lexicon Dump\n")
    md.append(f"Version: {data.get('version', 'N/A')}\n")
    md.append(f"Description: {data.get('description', 'N/A')}\n")
    md.append("\n## Vocabulary Table\n")
    md.append("| Term | Type | Meaning |")
    md.append("|---|---|---|")
    
    for item in data.get('words', []):
        term = item.get('term', '')
        t_type = item.get('type', '')
        meaning = item.get('meaning', '')
        md.append(f"| {term} | {t_type} | {meaning} |")
        
    return "\n".join(md)

def main():
    lexicon_path = '/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json'
    output_path = '/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/lexicon_dump.md'
    
    try:
        data = load_lexicon(lexicon_path)
        markdown_text = generate_markdown(data)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_text)
            
        print(f"Successfully dumped lexicon to {output_path}")
    except Exception as e:
        print(f"Error during lexicon dump: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
