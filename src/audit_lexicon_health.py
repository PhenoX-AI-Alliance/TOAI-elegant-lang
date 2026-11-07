import sys
import os
import traceback
import time
import json

def audit_lexicons():
    default_ws = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', default_ws)
    lexicon_dir = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    result = {
        "timestamp": time.time(),
        "core_status": "missing",
        "macro_status": "missing",
        "core_categories": {},
        "macro_categories": {},
        "core_compact_id_stats": {},
        "macro_compact_id_stats": {}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                result["core_status"] = "loaded"
                lex_dict = core_data.get('lexicon', {})
                categories = {}
                compact_ids = []
                for sym, data in lex_dict.items():
                    if isinstance(data, dict):
                        cat = data.get('category', 'unknown')
                        categories[cat] = categories.get(cat, 0) + 1
                        cid = data.get('compact_id')
                        if cid is not None:
                            compact_ids.append(cid)
                result["core_categories"] = categories
                result["core_compact_id_stats"] = {
                    "total_items": len(lex_dict),
                    "with_compact_id": len(compact_ids),
                    "min": min(compact_ids) if compact_ids else None,
                    "max": max(compact_ids) if compact_ids else None
                }
        except Exception as e:
            result["core_status"] = f"error: {str(e)}"
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                result["macro_status"] = "loaded"
                lex_dict = macro_data.get('lexicon', macro_data) if isinstance(macro_data, dict) else {}
                categories = {}
                compact_ids = []
                if isinstance(lex_dict, dict):
                    for sym, data in lex_dict.items():
                        if isinstance(data, dict):
                            cat = data.get('category', 'unknown')
                            categories[cat] = categories.get(cat, 0) + 1
                            cid = data.get('compact_id')
                            if cid is not None:
                                compact_ids.append(cid)
                result["macro_categories"] = categories
                result["macro_compact_id_stats"] = {
                    "total_items": len(lex_dict) if isinstance(lex_dict, dict) else 0,
                    "with_compact_id": len(compact_ids),
                    "min": min(compact_ids) if compact_ids else None,
                    "max": max(compact_ids) if compact_ids else None
                }
        except Exception as e:
            result["macro_status"] = f"error: {str(e)}"
            
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result

if __name__ == '__main__':
    try:
        audit_lexicons()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
