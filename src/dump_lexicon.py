import sys
import os
import json
import traceback

def load_lexicon(lexicon_path):
    if not os.path.exists(lexicon_path):
        raise FileNotFoundError(f"Lexicon file not found: {lexicon_path}")
    with open(lexicon_path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_markdown(lexicon_data):
    lines = ["# TOAI Elegant Lang - Core Lexicon", ""]
    lines.append("| Word / Token | Meaning / Description | Category |")
    lines.append("|---|---|---|")
    
    if isinstance(lexicon_data, dict):
        items = lexicon_data.items()
    elif isinstance(lexicon_data, list):
        items = enumerate(lexicon_data)
    else:
        items = []

    for key, val in items:
        if isinstance(val, dict):
            meaning = val.get("meaning", str(val))
            category = val.get("category", "general")
            lines.append(f"| `{key}` | {meaning} | {category} |")
        else:
            lines.append(f"| `{key}` | {val} | general |")
            
    return "\n".join(lines)

def main():
    try:
        lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
        if not os.path.exists(lexicon_path):
            os.makedirs(os.path.dirname(lexicon_path), exist_ok=True)
            default_data = {
                "gaia": {"meaning": "Earth Ecosystem / Altruistic Core", "category": "core"},
                "toai": {"meaning": "High-Precision TOAI Executor", "category": "core"}
            }
            with open(lexicon_path, "w", encoding="utf-8") as f:
                json.dump(default_data, f, ensure_ascii=False, indent=2)

        data = load_lexicon(lexicon_path)
        md_output = generate_markdown(data)
        
        output_md_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.md"
        with open(output_md_path, "w", encoding="utf-8") as f:
            f.write(md_output)
            
        print(md_output)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
