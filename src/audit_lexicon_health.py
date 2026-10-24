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
        print(f"Error loading {{filepath}}: {{e}}", file=sys.stderr)
        return {}

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    core_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon', 'core_lexicon.json')
    macro_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon', 'macro_lexicon.json')
    
    core_data = load_json(core_path)
    macro_data = load_json(macro_path)
    
    lexicon_dict = core_data.get('lexicon', {})
    
    categories = {}
    compact_ids = []
    
    for sym, data in lexicon_dict.items():
        if isinstance(data, dict):
            cat = data.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
            cid = data.get('compact_id')
            if cid is not None:
                compact_ids.append(cid)
                
    audit_result = {
        "core_lexicon_count": len(lexicon_dict),
        "macro_lexicon_count": len(macro_data) if isinstance(macro_data, dict) else 0,
        "category_distribution": categories,
        "compact_id_stats": {
            "total_compact_ids": len(compact_ids),
            "min_compact_id": min(compact_ids) if compact_ids else None,
            "max_compact_id": max(compact_ids) if compact_ids else None
        }
    }
    
    print(json.dumps(audit_result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        audit_lexicons()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
