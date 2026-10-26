import sys
import os
import json

def dump_lexicon():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/core_lexicon.md"
    
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {{lexicon_path}}", file=sys.stderr)
        sys.exit(1)
        
    with open(lexicon_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    lines = []
    lines.append("# TOAI-elegant-lang Core Lexicon")
    lines.append("")
    lines.append(f"**Version**: {{data.get('meta', {{}}).get('version', 'N/A')}}")
    lines.append("")
    lines.append("| Word | Category | Definition |")
    lines.append("|---|---|---|")
    
    for term in data.get("terms", []):
        lines.append(f"| {{term.get('word', '')}} | {{term.get('category', '')}} | {{term.get('definition', '')}} |")
        
    content = "\n".join(lines) + "\n"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Successfully generated lexicon markdown at {{output_path}}")

if __name__ == "__main__":
    dump_lexicon()
