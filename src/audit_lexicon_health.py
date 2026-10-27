import sys
import os
import json
import traceback

def load_json(filepath):
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}", file=sys.stderr)
        return {}

def audit_lexicon():
    base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(base_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    core_data = load_json(core_path)
    macro_data = load_json(macro_path)
    
    lexicon_entries = core_data.get('lexicon', {})
    if not lexicon_entries and isinstance(core_data, dict):
        lexicon_entries = core_data

    categories = {}
    compact_ids = []
    
    for sym, data in lexicon_entries.items():
        if isinstance(data, dict):
            cat = data.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
            if 'compact_id' in data:
                compact_ids.append(data.get('compact_id'))
                
    macro_categories = {}
    for sym, data in macro_data.items():
        if isinstance(data, dict):
            cat = data.get('category', 'unknown')
            macro_categories[cat] = macro_categories.get(cat, 0) + 1

    audit_result = {
        "core_total_entries": len(lexicon_entries),
        "core_category_distribution": categories,
        "core_compact_id_count": len(compact_ids),
        "macro_total_entries": len(macro_data),
        "macro_category_distribution": macro_categories
    }
    
    print(json.dumps(audit_result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        audit_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
