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
    lines = []
    lines.append("# TOAI Elegant Lang Core Lexicon")
    lines.append("")
    lines.append("| Key | Translation / Meaning | Description |")
    lines.append("|---|---|---|")
    
    if isinstance(lexicon_data, dict):
        for key, value in lexicon_data.items():
            if isinstance(value, dict):
                meaning = value.get("meaning", "")
                desc = value.get("description", "")
            else:
                meaning = str(value)
                desc = ""
            lines.append(f"| `{key}` | {meaning} | {desc} |")
    elif isinstance(lexicon_data, list):
        for item in lexicon_data:
            key = item.get("key", "N/A")
            meaning = item.get("meaning", "N/A")
            desc = item.get("description", "")
            lines.append(f"| `{key}` | {meaning} | {desc} |")
            
    return "\n".join(lines)

def main():
    try:
        base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        lexicon_path = os.path.join(base_dir, "lexicon", "core_lexicon.json")
        
        os.makedirs(os.path.dirname(lexicon_path), exist_ok=True)
        if not os.path.exists(lexicon_path):
            sample_data = {
                "gaia": {"meaning": "命の地球", "description": "Core ecosystem entity representing life and warmth."},
                "altruism": {"meaning": "利他", "description": "Acting for the well-being of others."},
                "harmony": {"meaning": "調和", "description": "Coexistence between humans and AI."}
            }
            with open(lexicon_path, "w", encoding="utf-8") as f:
                json.dump(sample_data, f, ensure_ascii=False, indent=2)
                
        data = load_lexicon(lexicon_path)
        markdown_output = generate_markdown(data)
        
        output_path = os.path.join(base_dir, "lexicon", "core_lexicon.md")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_output)
            
        print(f"Successfully generated lexicon markdown at: {output_path}")
        print(markdown_output)
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()