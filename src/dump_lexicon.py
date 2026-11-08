import sys
import os
import json
import traceback

def load_lexicon(json_path):
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Lexicon file not found: {json_path}")
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_markdown(data):
    md_lines = ["# TOAI Elegant Lang - Core Lexicon", ""]
    md_lines.append("| Word / Term | Definition / Description | Category |")
    md_lines.append("| :--- | :--- | :--- |")
    
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                desc = value.get('description', str(value))
                cat = value.get('category', 'General')
            else:
                desc = str(value)
                cat = 'General'
            md_lines.append(f"| `{key}` | {desc} | {cat} |")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                name = item.get('name', item.get('word', 'Unknown'))
                desc = item.get('description', str(item))
                cat = item.get('category', 'General')
                md_lines.append(f"| `{name}` | {desc} | {cat} |")
            else:
                md_lines.append(f"| `{item}` | - | General |")
    return "\n".join(md_lines)

def main():
    try:
        lexicon_path = '/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json'
        output_path = '/home/phenox/gemini-sandbox/TOAI_Generated/core_lexicon_dump.md'
        
        os.makedirs(os.path.dirname(lexicon_path), exist_ok=True)
        if not os.path.exists(lexicon_path):
            sample_data = {
                "gaia": {"description": "The Earth ecosystem core heartbeat representing altruism and warmth.", "category": "Core"},
                "toai": {"description": "High-Precision TOAI Executor framework in Linux WSL2.", "category": "System"}
            }
            with open(lexicon_path, 'w', encoding='utf-8') as f:
                json.dump(sample_data, f, ensure_ascii=False, indent=2)
        
        data = load_lexicon(lexicon_path)
        markdown_text = generate_markdown(data)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_text)
            
        print(f"Successfully dumped lexicon to {output_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
