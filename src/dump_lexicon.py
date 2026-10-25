import sys
import os
import traceback
import json

def dump_lexicon():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    output_path = "/home/phenox/gemini-sandbox/TOAI_Generated/core_lexicon_table.md"

    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}", file=sys.stderr)
        sys.exit(1)

    lines = []
    lines.append("# Core Lexicon Table")
    lines.append("")
    lines.append("| Term | Definition / Description | Category |")
    lines.append("|---|---|---|")

    if isinstance(data, dict):
        items = data.items()
    elif isinstance(data, list):
        items = [(str(i), item) for i, item in enumerate(data)]
    else:
        items = []

    for key, value in items:
        if isinstance(value, dict):
            desc = value.get("description", str(value))
            cat = value.get("category", "general")
        else:
            desc = str(value)
            cat = "general"
        lines.append(f"| {key} | {desc} | {cat} |")

    markdown_content = "\n".join(lines)
    print(markdown_content)

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"Successfully saved Markdown to {output_path}")
    except Exception as e:
        print(f"Error writing output file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    dump_lexicon()
