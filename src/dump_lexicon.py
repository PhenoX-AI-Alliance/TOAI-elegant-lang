import sys
import os
import json
import traceback

def load_lexicon(json_path):
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Lexicon file not found: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_markdown(data):
    lines = []
    lines.append("# Core Lexicon Summary")
    lines.append("")
    lines.append("| Word / Token | Category | Description |")
    lines.append("|---|---|---|")
    
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                category = value.get("category", "N/A")
                desc = value.get("description", str(value))
            else:
                category = "General"
                desc = str(value)
            lines.append(f"| `{key}` | {category} | {desc} |")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                key = item.get("word", item.get("name", "Unknown"))
                category = item.get("category", "N/A")
                desc = item.get("description", "")
                lines.append(f"| `{key}` | {category} | {desc} |")
            else:
                lines.append(f"| `{item}` | - | - |")
    else:
        lines.append(f"| - | - | {str(data)} |")
        
    return "\n".join(lines)

def main():
    try:
        base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        lexicon_path = os.path.join(base_dir, "lexicon", "core_lexicon.json")
        
        if not os.path.exists(lexicon_path):
            os.makedirs(os.path.dirname(lexicon_path), exist_ok=True)
            dummy_data = {
                "toai": {"category": "Core", "description": "The foundational AI entity identifier."},
                "elegance": {"category": "Quality", "description": "The measure of refined execution."}
            }
            with open(lexicon_path, "w", encoding="utf-8") as f:
                json.dump(dummy_data, f, indent=2, ensure_ascii=False)
                
        data = load_lexicon(lexicon_path)
        markdown_output = generate_markdown(data)
        
        output_md_path = os.path.join(base_dir, "lexicon_summary.md")
        with open(output_md_path, "w", encoding="utf-8") as f:
            f.write(markdown_output)
            
        print(markdown_output)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
