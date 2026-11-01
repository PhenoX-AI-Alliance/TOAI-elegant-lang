import sys
import os
import traceback
import json

def load_json(file_path):
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}", file=sys.stderr)
        return {}

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    core_data = load_json(core_path)
    macro_data = load_json(macro_path)
    
    lexicon_dict = core_data.get('lexicon', {})
    if not lexicon_dict and isinstance(core_data, dict):
        lexicon_dict = core_data
        
    categories = {}
    compact_ids = []
    
    for sym, data in lexicon_dict.items():
        if isinstance(data, dict):
            cat = data.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
            
            cid = data.get('compact_id')
            if cid is not None:
                compact_ids.append(cid)
                
    macro_categories = {}
    macro_dict = macro_data.get('lexicon', macro_data)
    if isinstance(macro_dict, dict):
        for sym, data in macro_dict.items():
            if isinstance(data, dict):
                cat = data.get('category', 'macro_unknown')
                macro_categories[cat] = macro_categories.get(cat, 0) + 1

    audit_result = {
        "timestamp": os.path.exists(core_path) and os.path.getmtime(core_path) or 0,
        "core_total_entries": len(lexicon_dict),
        "core_categories": categories,
        "compact_id_stats": {
            "total_count": len(compact_ids),
            "min": min(compact_ids) if compact_ids else None,
            "max": max(compact_ids) if compact_ids else None
        },
        "macro_total_entries": len(macro_dict) if isinstance(macro_dict, dict) else 0,
        "macro_categories": macro_categories
    }
    
    output_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'src', 'lexicon_audit_report.json')
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(audit_result, f, ensure_ascii=False, indent=2)
        print(f"Audit report successfully written to {output_path}")
    except Exception as e:
        print(f"Failed to write audit report: {e}", file=sys.stderr)
        sys.exit(1)
        
    print(json.dumps(audit_result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        audit_lexicons()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
