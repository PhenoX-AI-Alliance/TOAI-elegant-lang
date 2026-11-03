import sys
import os
import json

def load_lexicon(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Lexicon file not found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        if "lexicon" in data and isinstance(data["lexicon"], list):
            data = data["lexicon"]
        else:
            data = [data]
    if not isinstance(data, list):
        raise ValueError("Lexicon data must be a list of dictionaries.")
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Each lexicon entry must be a dictionary.")
    return data

def generate_markdown(data):
    lines = ["# Core Lexicon", "", "| Term | Category | Description |", "|---|---|---|"]
    for item in data:
        term = str(item.get("term", ""))
        category = str(item.get("category", ""))
        description = str(item.get("description", ""))
        lines.append(f"| {term} | {category} | {description} |")
    return "\n".join(lines)

def main():
    lexicon_path = "/home/phenox/gemini-sandbox/lexicon/core_lexicon.json"
    output_path = "/home/phenox/gemini-sandbox/TOAI_Generated/lexicon_report.md"
    try:
        data = load_lexicon(lexicon_path)
        md_content = generate_markdown(data)
        print(md_content)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"Successfully generated markdown report at {output_path}")
    except Exception as e:
        print(f"Error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
