import sys
import os
import json

def dump_lexicon():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    output_path = "/home/phenox/gemini-sandbox/TOAI_Generated/lexicon_dump.md"

    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
        sys.exit(1)

    lines = []
    lines.append("# Core Lexicon Dump")
    lines.append("")
    lines.append("| Term | Description | Category |")
    lines.append("|---|---|---|")

    items = data if isinstance(data, list) else data.get("items", [])
    if isinstance(data, dict) and not items:
        for k, v in data.items():
            desc = v.get("description", str(v)) if isinstance(v, dict) else str(v)
            cat = v.get("category", "General") if isinstance(v, dict) else "General"
            lines.append(f"| {k} | {desc} | {cat} |")
    elif isinstance(items, list):
        for item in items:
            if isinstance(item, dict):
                term = item.get("term", item.get("name", "Unknown"))
                desc = item.get("description", "")
                cat = item.get("category", "General")
                lines.append(f"| {term} | {desc} | {cat} |")
            else:
                lines.append(f"| {str(item)} | - | General |")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Successfully dumped lexicon to {output_path}")

if __name__ == "__main__":
    dump_lexicon()
