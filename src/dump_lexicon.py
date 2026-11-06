# -*- coding: utf-8 -*-
import sys
import os
import json
import traceback

def load_lexicon(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Lexicon file not found: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_markdown(data):
    md = []
    md.append("# TOAI Core Lexicon Reference")
    md.append("")
    md.append("This document contains the core lexicon of the TOAI-elegant-lang ecosystem.")
    md.append("")
    md.append("| Key | Value / Description |")
    md.append("|---|---|")
    
    if isinstance(data, dict):
        for k, v in data.items():
            val_str = str(v).replace("|", "\\|").replace("\n", " ")
            md.append(f"| `{k}` | {val_str} |")
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            val_str = str(item).replace("|", "\\|").replace("\n", " ")
            md.append(f"| {idx} | {val_str} |")
    else:
        md.append(f"| Data | {str(data)} |")
        
    return "\n".join(md)

def main():
    lexicon_path = '/home/phenox/gemini-sandbox/lexicon/core_lexicon.json'
    try:
        data = load_lexicon(lexicon_path)
        markdown_output = generate_markdown(data)
        print(markdown_output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
