import sys
import os
import json
import traceback

def load_lexicon(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Lexicon file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_markdown(data):
    lines = ["# TOAI Elegant Lang - Core Lexicon", ""]
    if isinstance(data, dict):
        version = data.get("version", "Unknown")
        lines.append(f"**Version:** {version}")
        lines.append("")
        lexicon = data.get("lexicon", [])
    elif isinstance(data, list):
        lexicon = data
    else:
        lexicon = []
        
    lines.append("| Term | Definition |")
    lines.append("|---|---|")
    for item in lexicon:
        term = item.get("term", "")
        defn = item.get("definition", "")
        lines.append(f"| {term} | {defn} |")
    return "\n".join(lines)

def main():
    try:
        lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
        data = load_lexicon(lexicon_path)
        md_output = generate_markdown(data)
        
        output_path = "/home/phenox/gemini-sandbox/TOAI_Generated/lexicon_table.md"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_output)
            
        print(md_output)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
