import sys
import os
import traceback
import time
import json

def dump_lexicon():
    try:
        lexicon_path = '/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json'
        if not os.path.exists(lexicon_path):
            print(f"Error: Lexicon file not found at {{lexicon_path}}", file=sys.stderr)
            sys.exit(1)
            
        with open(lexicon_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        print("# TOAI Elegant Lang - Lexicon Dump")
        print(f"Version: {{data.get('version', 'N/A')}}")
        print(f"Ecosystem: {{data.get('ecosystem', 'N/A')}}\n")
        print("| Term | Category | Description |")
        print("|---|---|---|")
        
        words = data.get('words', [])
        for item in words:
            term = item.get('term', '')
            category = item.get('category', '')
            desc = item.get('description', '')
            print(f"| {{term}} | {{category}} | {{desc}} |")
            
        output_md_path = '/home/phenox/gemini-sandbox/TOAI_Generated/lexicon_dump.md'
        with open(output_md_path, 'w', encoding='utf-8') as out:
            out.write("# TOAI Elegant Lang - Lexicon Dump\n")
            out.write(f"Version: {{data.get('version', 'N/A')}}\n")
            out.write(f"Ecosystem: {{data.get('ecosystem', 'N/A')}}\n\n")
            out.write("| Term | Category | Description |\n")
            out.write("|---|---|---|\n")
            for item in words:
                term = item.get('term', '')
                category = item.get('category', '')
                desc = item.get('description', '')
                out.write(f"| {{term}} | {{category}} | {{desc}} |\n")
        print(f"Successfully dumped lexicon to {{output_md_path}}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    dump_lexicon()
