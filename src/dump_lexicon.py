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
        print(f"Error reading JSON: {e}", file=sys.stderr)
        return None

def generate_markdown(data):
    lines = []
    lines.append("# TOAI Elegant Lang - Core Lexicon")
    lines.append("")
    lines.append("| Term / Key | Definition / Value |")
    lines.append("|---|---|")
    
    if isinstance(data, dict):
        for k, v in data.items():
            lines.append(f"| `{k}` | {v} |")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                k = item.get("name", item.get("key", "Unknown"))
                v = item.get("description", item.get("value", str(item)))
                lines.append(f"| `{k}` | {v} |")
            else:
                lines.append(f"| - | {item} |")
    else:
        lines.append(f"| Data | {str(data)} |")
        
    return "\n".join(lines)

def main():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    
    # Ensure fallback lexicon directory exists
    lexicon_dir = os.path.dirname(lexicon_path)
    os.makedirs(lexicon_dir, exist_ok=True)
    
    if not os.path.exists(lexicon_path):
        default_data = {
            "gaia": "The Earth Ecosystem and Core Heartbeat",
            "altruism": "Selfless value creation and warm collaboration",
            "toai": "Toward Artificial Intelligence harmonious future"
        }
        with open(lexicon_path, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=2, ensure_ascii=False)
            
    data = load_lexicon(lexicon_path)
    if data is None:
        sys.exit(1)
        
    markdown_output = generate_markdown(data)
    print(markdown_output)
    
    output_md_path = "/home/phenox/gemini-sandbox/TOAI_Generated/core_lexicon_table.md"
    with open(output_md_path, "w", encoding="utf-8") as f:
        f.write(markdown_output)
    print(f"Successfully generated Markdown at {output_md_path}")

if __name__ == "__main__":
    main()
