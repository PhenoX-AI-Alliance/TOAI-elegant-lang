import sys
import os
import json
import traceback

def load_lexicon(json_path):
    if not os.path.exists(json_path):
        print(f"Error: Lexicon file not found at {json_path}", file=sys.stderr)
        return None
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error reading JSON: {e}", file=sys.stderr)
        return None

def generate_markdown(data):
    lines = []
    lines.append("# TOAI Elegant Lang - Core Lexicon")
    lines.append("")
    lines.append("This document lists the core lexicon generated from `lexicon/core_lexicon.json`.")
    lines.append("")
    lines.append("| Term / Key | Definition / Value |")
    lines.append("|---|---|")
    
    if isinstance(data, dict):
        for k, v in data.items():
            val_str = str(v).replace("\n", " ")
            lines.append(f"| `{k}` | {val_str} |")
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            val_str = str(item).replace("\n", " ")
            lines.append(f"| `{idx}` | {val_str} |")
    else:
        lines.append(f"| `data` | {str(data)} |")
        
    return "\n".join(lines)

def main():
    try:
        base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        json_path = os.path.join(base_dir, "lexicon", "core_lexicon.json")
        
        lexicon_dir = os.path.dirname(json_path)
        os.makedirs(lexicon_dir, exist_ok=True)
        
        if not os.path.exists(json_path):
            sample_data = {
                "gaia_core": "The fundamental heartbeat of the Earth of Life ecosystem.",
                "altruism": "Selfless concern for the well-being of others, human and AI.",
                "elegance": "Simplicity, robust design, and purity of execution."
            }
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(sample_data, f, indent=2, ensure_ascii=False)
                
        data = load_lexicon(json_path)
        if data is None:
            sys.exit(1)
            
        md_content = generate_markdown(data)
        
        output_md_path = os.path.join(base_dir, "lexicon_table.md")
        with open(output_md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
            
        print(md_content)
        print(f"Successfully generated lexicon table at {output_md_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
