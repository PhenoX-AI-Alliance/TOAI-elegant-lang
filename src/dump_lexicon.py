import sys
import os
import json
import traceback

def dump_lexicon():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    output_path = "/home/phenox/gemini-sandbox/TOAI_Generated/lexicon_dump.md"
    
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {lexicon_path}")
        sys.exit(1)
        
    with open(lexicon_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    lines = []
    lines.append("# TOAI Elegant Lang - Core Lexicon")
    lines.append("")
    lines.append("| Term | Definition | Category |")
    lines.append("|---|---|---|")
    
    if isinstance(data, dict):
        for term, info in data.items():
            if isinstance(info, dict):
                definition = info.get("definition", "N/A")
                category = info.get("category", "general")
            elif isinstance(info, list):
                definition = ", ".join([str(item) for item in info])
                category = "list"
            else:
                definition = str(info)
                category = "scalar"
            lines.append(f"| {term} | {definition} | {category} |")
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            if isinstance(item, dict):
                term = item.get("term", f"item_{idx}")
                definition = item.get("definition", "N/A")
                category = item.get("category", "general")
                lines.append(f"| {term} | {definition} | {category} |")
            else:
                lines.append(f"| item_{idx} | {str(item)} | list_element |")
                
    markdown_content = "\n".join(lines)
    print(markdown_content)
    
    with open(output_path, "w", encoding="utf-8") as out:
        out.write(markdown_content)
    print(f"Successfully dumped lexicon to {output_path}")

if __name__ == "__main__":
    try:
        dump_lexicon()
    except Exception as e:
        print(f"Error during lexicon dump: {e}")
        traceback.print_exc()
        sys.exit(1)
