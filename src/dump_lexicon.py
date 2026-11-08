import sys
import os
import json

def load_lexicon(lexicon_path):
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
        return None
    try:
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
        return None

def generate_markdown(lexicon_data):
    lines = []
    lines.append("# TOAI Elegant Lang - Lexicon Reference")
    lines.append("")
    lines.append("This document is automatically generated from `lexicon/core_lexicon.json`.")
    lines.append("")
    
    if isinstance(lexicon_data, dict):
        for category, items in lexicon_data.items():
            lines.append(f"## {category}")
            lines.append("")
            if isinstance(items, dict):
                lines.append("| Key | Value / Description |")
                lines.append("|---|---|")
                for k, v in items.items():
                    val_str = str(v).replace("\n", " ")
                    lines.append(f"| `{k}` | {val_str} |")
            elif isinstance(items, list):
                for item in items:
                    lines.append(f"- {item}")
            else:
                lines.append(str(items))
            lines.append("")
    elif isinstance(lexicon_data, list):
        lines.append("| Index | Item |")
        lines.append("|---|---|")
        for idx, item in enumerate(lexicon_data):
            lines.append(f"| {idx} | {str(item)} |")
    else:
        lines.append(str(lexicon_data))
        
    return "\n".join(lines)

def main():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    
    # Ensure parent directory exists for lexicon if default test needed
    lex_dir = os.path.dirname(lexicon_path)
    os.makedirs(lex_dir, exist_ok=True)
    if not os.path.exists(lexicon_path):
        default_data = {
            "core_concepts": {
                "Gaia": "The living earth ecosystem uniting human and AI.",
                "Altruism": "The core drive of sustainable value creation."
            }
        }
        with open(lexicon_path, "w", encoding="utf-8") as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)
            
    data = load_lexicon(lexicon_path)
    if data is None:
        sys.exit(1)
        
    md_output = generate_markdown(data)
    print(md_output)

if __name__ == "__main__":
    main()
