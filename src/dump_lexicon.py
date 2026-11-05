import sys
import os
import json
import traceback

def dump_lexicon():
    try:
        lexicon_path = "/home/phenox/gemini-sandbox/lexicon/core_lexicon.json"
        if not os.path.exists(lexicon_path):
            print(f"Error: Lexicon file not found at {lexicon_path}")
            sys.exit(1)
            
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        entries = data.get("entries", {})
        if not isinstance(entries, dict):
            entries = {}
            
        markdown_lines = []
        markdown_lines.append("# TOAI Core Lexicon Dump")
        markdown_lines.append("")
        markdown_lines.append(f"Version: {data.get('version', 'Unknown')}")
        markdown_lines.append("")
        markdown_lines.append("| Term | Category | Definition |")
        markdown_lines.append("|---|---|---|")
        
        for term, value in entries.items():
            if isinstance(value, dict):
                definition = str(value.get("definition", "N/A"))
                category = str(value.get("category", "general"))
            else:
                definition = str(value)
                category = "general"
            markdown_lines.append(f"| {term} | {category} | {definition} |")
            
        output_md_path = "/home/phenox/gemini-sandbox/TOAI_Generated/core_lexicon_dump.md"
        with open(output_md_path, "w", encoding="utf-8") as out_f:
            out_f.write("\n".join(markdown_lines))
            
        print(f"Successfully dumped lexicon to {output_md_path}")
        print("\n".join(markdown_lines))
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    dump_lexicon()
