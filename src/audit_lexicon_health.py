import sys
import os
import traceback
import json

def load_json(filepath):
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
        return {}

def audit_lexicon():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
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
        else:
            categories['unknown'] = categories.get('unknown', 0) + 1
            
    macro_count = len(macro_data) if isinstance(macro_data, (dict, list)) else 0
    
    audit_result = {
        "total_core_symbols": len(lexicon_dict),
        "category_distribution": categories,
        "compact_id_stats": {
            "total_count": len(compact_ids),
            "min": min(compact_ids) if compact_ids else None,
            "max": max(compact_ids) if compact_ids else None
        },
        "macro_lexicon_entries": macro_count
    }
    
    print(json.dumps(audit_result, ensure_ascii=False, indent=2))
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    out_file = os.path.join(output_dir, 'lexicon_audit_report.json')
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(audit_result, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    try:
        audit_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
