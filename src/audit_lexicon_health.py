import sys
import os
import traceback
import time
import json

def load_json_file(filepath):
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
        return None

def audit_lexicon():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    core_data = load_json_file(core_path)
    macro_data = load_json_file(macro_path)
    
    audit_result = {
        "timestamp": time.time(),
        "core_lexicon_status": "missing" if core_data is None else "loaded",
        "macro_lexicon_status": "missing" if macro_data is None else "loaded",
        "core_categories": {},
        "core_compact_id_stats": {},
        "macro_categories": {},
        "macro_compact_id_stats": {}
    }
    
    if core_data and isinstance(core_data, dict):
        lexicon_dict = core_data.get('lexicon', core_data)
        if isinstance(lexicon_dict, dict):
            categories = {}
            compact_ids = []
            for sym, data in lexicon_dict.items():
                if isinstance(data, dict):
                    cat = data.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    cid = data.get('compact_id')
                    if cid is not None:
                        compact_ids.append(cid)
            audit_result["core_categories"] = categories
            audit_result["core_compact_id_stats"] = {
                "total_count": len(compact_ids),
                "unique_count": len(set(compact_ids))
            }
            
    if macro_data and isinstance(macro_data, dict):
        macro_dict = macro_data.get('lexicon', macro_data)
        if isinstance(macro_dict, dict):
            categories = {}
            compact_ids = []
            for sym, data in macro_dict.items():
                if isinstance(data, dict):
                    cat = data.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    cid = data.get('compact_id')
                    if cid is not None:
                        compact_ids.append(cid)
            audit_result["macro_categories"] = categories
            audit_result["macro_compact_id_stats"] = {
                "total_count": len(compact_ids),
                "unique_count": len(set(compact_ids))
            }
            
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'lexicon_audit_report.json')
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(audit_result, f, ensure_ascii=False, indent=2)
        print(f"Audit report successfully written to {output_path}")
    except Exception as e:
        print(f"Failed to write audit report: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    try:
        audit_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
