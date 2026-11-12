import sys
import os
import json

def load_lexicon(file_path):
    if not os.path.exists(file_path):
        print(f"Error: Lexicon file not found at {file_path}", file=sys.stderr)
        sys.exit(1)
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_markdown(data):
    md = ["# TOAI Elegant Lang - Core Lexicon", ""]
    md.append("| Key | Type / Value | Description |")
    md.append("|---|---|---|")
    
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                desc = value.get("description", "N/A")
                val_str = str(value.get("value", ""))
            else:
                desc = "N/A"
                val_str = str(value)
            md.append(f"| `{key}` | `{val_str}` | {desc} |")
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            if isinstance(item, dict):
                desc = item.get("description", "N/A")
                val_str = str(item.get("value", ""))
            else:
                desc = "N/A"
                val_str = str(item)
            md.append(f"| [{idx}] | `{val_str}` | {desc} |")
    else:
        md.append(f"| Root | `{str(data)}` | N/A |")
        
    return "\n".join(md)

def main():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    
    # fallback to local sandbox if not found
    if not os.path.exists(lexicon_path):
        fallback_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon"
        os.makedirs(fallback_dir, exist_ok=True)
        lexicon_path = os.path.join(fallback_dir, "core_lexicon.json")
        if not os.path.exists(lexicon_path):
            sample_data = {
                "alpha": {"value": "1", "description": "First element"},
                "beta": {"value": "2", "description": "Second element"},
                "simple_key": "raw_string_value"
            }
            with open(lexicon_path, "w", encoding="utf-8") as f:
                json.dump(sample_data, f, indent=2, ensure_ascii=False)
                
    data = load_lexicon(lexicon_path)
    markdown_output = generate_markdown(data)
    
    output_md_path = "/home/phenox/gemini-sandbox/TOAI_Generated/core_lexicon.md"
    with open(output_md_path, "w", encoding="utf-8") as f:
        f.write(markdown_output)
        
    print(markdown_output)

if __name__ == "__main__":
    main()
