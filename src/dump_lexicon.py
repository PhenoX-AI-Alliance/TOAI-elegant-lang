import sys
import os
import json
import traceback

def main():
    lexicon_path = '/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json'
    output_path = '/home/phenox/gemini-sandbox/TOAI_Generated/lexicon_table.md'
    
    try:
        if not os.path.exists(lexicon_path):
            print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
            sys.exit(1)
            
        with open(lexicon_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        lines = []
        lines.append("# TOAI Core Lexicon Dump")
        lines.append("")
        lines.append("| Word / Symbol | Meaning / Description | Category |")
        lines.append("|---|---|---|")
        
        items = data if isinstance(data, list) else data.get('lexicon', [])
        
        for item in items:
            word = str(item.get('word', ''))
            meaning = str(item.get('meaning', ''))
            category = str(item.get('category', 'general'))
            lines.append(f"| {word} | {meaning} | {category} |")
            
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines) + "\n")
            
        print(f"Successfully dumped lexicon to {output_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
