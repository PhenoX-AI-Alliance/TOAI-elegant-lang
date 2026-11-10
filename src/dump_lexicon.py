import sys
import os
import json

def load_lexicon(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Lexicon file not found at {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_markdown(data):
    lines = []
    lines.append("# TOAI Core Lexicon")
    lines.append("")
    lines.append(f"- **Version**: {data.get('version', 'N/A')}")
    lines.append(f"- **Description**: {data.get('description', 'N/A')}")
    lines.append("")
    lines.append("## Vocabulary Table")
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
    lexicon_path = "/home/phenox/gemini-sandbox/lexicon/core_lexicon.json"
    try:
        data = load_lexicon(lexicon_path)
        md_output = generate_markdown(data)
        
        output_file = "/home/phenox/gemini-sandbox/TOAI_Generated/lexicon_output.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(md_output)
            
        print(md_output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
