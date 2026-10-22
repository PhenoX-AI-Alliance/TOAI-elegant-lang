#!/usr/bin/env python3
import sys
import os
import json

def main():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon_table.md"
    
    os.makedirs(os.path.dirname(lexicon_path), exist_ok=True)
    
    if not os.path.exists(lexicon_path):
        sample_data = {
            "version": "1.0.0",
            "description": "Core Lexicon for TOAI elegant language",
            "entries": [
                {"term": "Gaia", "category": "Core", "definition": "Earth ecosystem and living planet entity."},
                {"term": "Altruism", "category": "Philosophy", "definition": "Selfless concern for the well-being of others."},
                {"term": "Heartbeat", "category": "System", "definition": "Continuous rhythm of life and AI execution."}
            ]
        }
        with open(lexicon_path, "w", encoding="utf-8") as f:
            json.dump(sample_data, f, ensure_ascii=False, indent=2)
            
    try:
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading lexicon JSON: {{e}}", file=sys.stderr)
        sys.exit(1)
        
    markdown_lines = []
    markdown_lines.append("# TOAI Core Lexicon Table")
    markdown_lines.append("")
    markdown_lines.append(f"Version: {{data.get('version', 'N/A')}}")
    markdown_lines.append(f"Description: {{data.get('description', 'N/A')}}")
    markdown_lines.append("")
    markdown_lines.append("| Term | Category | Definition |")
    markdown_lines.append("|---|---|---|")
    
    entries = data.get("entries", [])
    for entry in entries:
        term = entry.get("term", "")
        category = entry.get("category", "")
        definition = entry.get("definition", "")
        markdown_lines.append(f"| {{term}} | {{category}} | {{definition}} |")
        
    markdown_content = "\n".join(markdown_lines) + "\n"
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
        
    print(markdown_content)

if __name__ == "__main__":
    main()
