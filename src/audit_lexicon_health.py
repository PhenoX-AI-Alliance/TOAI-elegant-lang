import sys
import os
import json

def audit():
    base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(base_dir, 'lexicon')
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    if not os.path.exists(core_path) or not os.path.exists(macro_path):
        print("Lexicon files not found.")
        sys.exit(1)
        
    with open(core_path, 'r', encoding='utf-8') as f:
        core = json.load(f)
    with open(macro_path, 'r', encoding='utf-8') as f:
        macro = json.load(f)
        
    categories = {}
    ids = []
    
    for k, v in core.get('lexicon', {}).items():
        if isinstance(v, dict):
            cat = v.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
            if 'compact_id' in v:
                ids.append(v['compact_id'])
                
    for k, v in macro.get('macro_lexicon', {}).items():
        if isinstance(v, dict):
            cat = v.get('category', 'macro')
            categories[cat] = categories.get(cat, 0) + 1
            if 'compact_id' in v:
                ids.append(v['compact_id'])
                
    report = {
        "categories": categories,
        "compact_id_count": len(ids),
        "min_id": min(ids) if ids else None,
        "max_id": max(ids) if ids else None
    }
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    audit()
