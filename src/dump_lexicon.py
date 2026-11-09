import sys
import os
import traceback
import json

def load_lexicon(lexicon_path):
    if not os.path.exists(lexicon_path):
        raise FileNotFoundError(f"Lexicon file not found: {lexicon_path}")
    with open(lexicon_path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_markdown(data):
    lines = []
    lines.append("# Core Lexicon Summary")
    lines.append("")
    lines.append("| Term | Definition / Category |")
    lines.append("|---|---|")
    
    if isinstance(data, dict):
        for key, value in data.items():
            lines.append(f"| `{key}` | {str(value)} |")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                term = item.get("term", item.get("name", "Unknown"))
                desc = item.get("description", item.get("category", ""))
                lines.append(f"| `{term}` | {desc} |")
            else:
                lines.append(f"| `{str(item)}` | - |")
    else:
        lines.append(f"| Raw Data | {str(data)} |")
        
    return "\n".join(lines)

def main():
    try:
        lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
        
        if not os.path.exists(lexicon_path):
            os.makedirs(os.path.dirname(lexicon_path), exist_ok=True)
            default_data = {
                "gaia_core": "The heart of life ecosystem, ensuring altruism and sustainability.",
                "toai_executor": "High-precision agent executing tasks securely in Linux environments.",
                "altruistic_monetization": "Sustainable value generation providing genuine utility."
            }
            with open(lexicon_path, "w", encoding="utf-8") as f:
                json.dump(default_data, f, ensure_ascii=False, indent=2)
                
        lexicon_data = load_lexicon(lexicon_path)
        markdown_output = generate_markdown(lexicon_data)
        
        output_path = "/home/phenox/gemini-sandbox/TOAI_Generated/lexicon_summary.md"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_output)
            
        print(f"Successfully generated lexicon summary at: {output_path}")
        print(markdown_output)
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
