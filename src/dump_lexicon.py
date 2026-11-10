import sys
import os
import json

def load_lexicon(file_path):
    if not os.path.exists(file_path):
        print(f"Error: Lexicon file not found at {{file_path}}", file=sys.stderr)
        sys.exit(1)
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_markdown(data):
    lines = []
    lines.append("# TOAI Core Lexicon\\n")
    lines.append(f"Version: {{data.get('version', 'N/A')}}\\\n")
    lines.append(f"Description: {{data.get('description', 'N/A')}}\\\n")
    lines.append("| Term | Category | Definition |")
    lines.append("|---|---|---|")
    for entry in data.get('entries', []):
        term = entry.get('term', '')
        category = entry.get('category', '')
        definition = entry.get('definition', '')
        lines.append(f"| {{term}} | {{category}} | {{definition}} |")
    return "\\n".join(lines)

def main():
    base_path = '/home/phenox/gemini-sandbox'
    lexicon_path = os.path.join(base_path, 'lexicon', 'core_lexicon.json')
    data = load_lexicon(lexicon_path)
    md_output = generate_markdown(data)
    
    output_dir = os.path.join(base_path, 'TOAI-elegant-lang', 'output')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'lexicon_table.md')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md_output)
    
    print(md_output)

if __name__ == '__main__':
    main()
