import sys
import os
import traceback
import json

def dump_lexicon():
    try:
        lexicon_path = '/home/phenox/gemini-sandbox/lexicon/core_lexicon.json'
        if not os.path.exists(lexicon_path):
            print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
            sys.exit(1)
            
        with open(lexicon_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        lines = []
        lines.append("# TOAI Core Lexicon Dump")
        lines.append("")
        lines.append(f"Version: {data.get('version', 'Unknown')}")
        lines.append(f"Description: {data.get('description', '')}")
        lines.append("")
        lines.append("| Term | Type | Meaning |")
        lines.append("|---|---|---|")
        
        for item in data.get('words', []):
            term = item.get('term', '')
            t_type = item.get('type', '')
            meaning = item.get('meaning', '')
            lines.append(f"| {term} | {t_type} | {meaning} |")
            
        output_markdown = "\n".join(lines)
        print(output_markdown)
        
        out_path = '/home/phenox/gemini-sandbox/TOAI_Generated/lexicon_dump.md'
        with open(out_path, 'w', encoding='utf-8') as out_f:
            out_f.write(output_markdown)
            
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    dump_lexicon()