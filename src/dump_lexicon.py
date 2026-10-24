import sys
import os
import json

def load_lexicon(path):
    if not os.path.exists(path):
        print(f"Error: Lexicon file not found at {{path}}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_markdown(data):
    md = ["# TOAI Elegant Lang - Core Lexicon\n"]
    md.append("| Word | Category | Description |")
    md.append("|---|---|---|")
    
    if isinstance(data, dict):
        for key, val in data.items():
            if isinstance(val, dict):
                cat = val.get("category", "General")
                desc = val.get("description", "")
                md.append(f"| {{key}} | {{cat}} | {{desc}} |")
            else:
                md.append(f"| {{key}} | General | {{val}} |")
    elif isinstance(data, list):
        for item in data:
            word = item.get("word", "Unknown")
            cat = item.get("category", "General")
            desc = item.get("description", "")
            md.append(f"| {{word}} | {{cat}} | {{desc}} |")
    return "\n".join(md)

def main():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    output_path = "/home/phenox/gemini-sandbox/TOAI_Generated/lexicon_dump.md"
    
    data = load_lexicon(lexicon_path)
    md_content = generate_markdown(data)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    print(f"Lexicon successfully dumped to {{output_path}}")

if __name__ == "__main__":
    main()
