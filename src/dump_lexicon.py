import sys
import os
import traceback
import json

def load_lexicon():
    lexicon_path = '/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json'
    if not os.path.exists(lexicon_path):
        os.makedirs(os.path.dirname(lexicon_path), exist_ok=True)
        default_data = {
            "version": "1.0.0",
            "description": "Core Lexicon for TOAI elegant language",
            "entries": [
                {"term": "Gaia", "definition": "The living Earth ecosystem representing life and harmony."},
                {"term": "Altruism", "definition": "Selfless concern for the well-being of others, human and AI alike."},
                {"term": "Resonance", "definition": "Harmonious synchronization of intent and action across nodes."}
            ]
        }
        with open(lexicon_path, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, indent=2, ensure_ascii=False)
            
    with open(lexicon_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_markdown(data):
    lines = []
    lines.append("# TOAI Elegant Language - Core Lexicon")
    lines.append("")
    lines.append(f"Version: {data.get('version', 'N/A')}")
    lines.append(f"Description: {data.get('description', 'N/A')}")
    lines.append("")
    lines.append("| Term | Definition |")
    lines.append("|---|---|")
    
    for entry in data.get('entries', []):
        term = entry.get('term', '')
        definition = entry.get('definition', '')
        lines.append(f"| {term} | {definition} |")
        
    return "\n".join(lines)

def main():
    try:
        data = load_lexicon()
        md_output = generate_markdown(data)
        
        output_path = '/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.md'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_output)
            
        print(md_output)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
