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
    lines.append("# TOAI-elegant-lang Core Lexicon")
    lines.append("")
    lines.append(f"**Version:** {data.get('version', 'N/A')}  ")
    lines.append(f"**Description:** {data.get('description', 'N/A')}  ")
    lines.append("")
    lines.append("## Vocabulary Table")
    lines.append("")
    lines.append("| Term | Meaning | Category |")
    lines.append("| :--- | :--- | :--- |")
    
    words = data.get("words", [])
    for item in words:
        term = item.get("term", "")
        meaning = item.get("meaning", "")
        category = item.get("category", "")
        lines.append(f"| `{term}` | {meaning} | {category} |")
        
    return "\n".join(lines)

def main():
    try:
        lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
        data = load_lexicon(lexicon_path)
        md_content = generate_markdown(data)
        
        output_path = "/home/phenox/gemini-sandbox/TOAI_Generated/core_lexicon_table.md"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)
            
        print(f"Successfully generated lexicon markdown at: {output_path}")
        print(md_content)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
