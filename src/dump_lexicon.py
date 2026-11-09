import sys
import os
import json
import traceback

def load_lexicon(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Lexicon file not found: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_markdown(data):
    lines = []
    lines.append("# TOAI Elegant Language - Core Lexicon")
    lines.append("")
    lines.append(f"Version: {data.get('version', 'N/A')}")
    lines.append(f"Description: {data.get('description', 'N/A')}")
    lines.append("")
    lines.append("| Term | Type | Meaning |")
    lines.append("|---|---|---|")
    
    entries = data.get("entries", [])
    for entry in entries:
        term = entry.get("term", "")
        t_type = entry.get("type", "")
        meaning = entry.get("meaning", "")
        lines.append(f"| {term} | {t_type} | {meaning} |")
        
    return "\n".join(lines)

def main():
    try:
        base_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        lexicon_path = os.path.join(base_path, "lexicon", "core_lexicon.json")
        output_path = os.path.join(base_path, "lexicon", "core_lexicon.md")
        
        data = load_lexicon(lexicon_path)
        markdown_text = generate_markdown(data)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_text)
            
        print(markdown_text)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
