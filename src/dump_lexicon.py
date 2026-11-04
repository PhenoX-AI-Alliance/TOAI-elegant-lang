import sys
import os
import json

def load_lexicon(file_path):
    if not os.path.exists(file_path):
        print(f"Error: Lexicon file not found at {{file_path}}", file=sys.stderr)
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading lexicon JSON: {{e}}", file=sys.stderr)
        sys.exit(1)

def generate_markdown(lexicon_data):
    md = ["# TOAI Elegant Lang - Core Lexicon\n"]
    md.append("| Term | Definition / Meaning | Category |")
    md.append("|---|---|---|")
    
    if isinstance(lexicon_data, dict):
        for key, value in lexicon_data.items():
            if isinstance(value, dict):
                defn = value.get("definition", str(value))
                cat = value.get("category", "general")
            else:
                defn = str(value)
                cat = "general"
            md.append(f"| {{key}} | {{defn}} | {{cat}} |")
    elif isinstance(lexicon_data, list):
        for item in lexicon_data:
            term = item.get("term", "unknown")
            defn = item.get("definition", "")
            cat = item.get("category", "general")
            md.append(f"| {{term}} | {{defn}} | {{cat}} |")
            
    return "\n".join(md)

def main():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    
    os.makedirs(os.path.dirname(lexicon_path), exist_ok=True)
    if not os.path.exists(lexicon_path):
        sample_data = {
            "gaia": {"definition": "The living Earth ecosystem", "category": "core"},
            "altruism": {"definition": "Selfless concern for the well-being of others", "category": "ethics"},
            "resonance": {"definition": "Harmonious synchronization of AI and human intent", "category": "tech"}
        }
        with open(lexicon_path, "w", encoding="utf-8") as f:
            json.dump(sample_data, f, indent=2, ensure_ascii=False)
            
    data = load_lexicon(lexicon_path)
    markdown_output = generate_markdown(data)
    
    print(markdown_output)
    
    out_md_path = "/home/phenox/gemini-sandbox/TOAI_Generated/core_lexicon_table.md"
    with open(out_md_path, "w", encoding="utf-8") as f:
        f.write(markdown_output)
    print(f"Successfully saved Markdown lexicon to {{out_md_path}}")

if __name__ == "__main__":
    main()
