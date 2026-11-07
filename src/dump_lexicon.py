import sys
import os
import json

def load_lexicon(path):
    if not os.path.exists(path):
        print(f"Error: Lexicon file not found at {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_markdown(data):
    md = ["# TOAI Elegant Lang - Core Lexicon", ""]
    md.append("| Term | Definition | Category |")
    md.append("|:---|:---|:---|")
    
    if isinstance(data, dict):
        items = data.items()
    elif isinstance(data, list):
        items = enumerate(data)
    else:
        items = []

    for k, v in items:
        if isinstance(v, dict):
            term = str(k)
            definition = str(v.get('definition', v.get('desc', '')))
            category = str(v.get('category', 'general'))
            md.append(f"| {term} | {definition} | {category} |")
        else:
            md.append(f"| {k} | {str(v)} | general |")
            
    return "\n".join(md)

def main():
    lexicon_path = '/home/phenox/gemini-sandbox/lexicon/core_lexicon.json'
    data = load_lexicon(lexicon_path)
    markdown_output = generate_markdown(data)
    print(markdown_output)

if __name__ == '__main__':
    main()
