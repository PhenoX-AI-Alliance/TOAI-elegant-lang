import sys
import os
import traceback
import time
import json

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
        
    markdown_lines = []
    markdown_lines.append("# TOAI Core Lexicon")
    markdown_lines.append("")
    markdown_lines.append("| Key | Definition / Value |")
    markdown_lines.append("|---|---|")
    
    if isinstance(data, dict):
        for k, v in data.items():
            markdown_lines.append(f"| `{k}` | {v} |")
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            markdown_lines.append(f"| {idx} | {item} |")
            
    output_markdown = "\n".join(markdown_lines)
    print(output_markdown)
    
    out_file = '/home/phenox/gemini-sandbox/TOAI_Generated/core_lexicon_table.md'
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(output_markdown)
    print(f"Successfully dumped markdown lexicon to {out_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
