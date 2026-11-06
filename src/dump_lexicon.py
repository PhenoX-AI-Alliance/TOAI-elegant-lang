import sys
import os
import json

def dump_lexicon():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
        sys.exit(1)
        
    with open(lexicon_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    markdown_lines = ["# TOAI Core Lexicon\n", "| Word | Definition | Category |", "|---|---|---|"]
    
    for word, details in data.items():
        if isinstance(details, dict):
            definition = details.get("definition", "N/A")
            category = details.get("category", "N/A")
        else:
            definition = str(details)
            category = "N/A"
        markdown_lines.append(f"| {word} | {definition} | {category} |")
        
    output_markdown = "\n".join(markdown_lines)
    print(output_markdown)
    
    out_file = "/home/phenox/gemini-sandbox/TOAI_Generated/lexicon_table.md"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(output_markdown)

if __name__ == "__main__":
    dump_lexicon()
