import sys
import os
import json
import traceback

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    result = {
        "core_lexicon": {},
        "macro_lexicon": {}
    }
    
    try:
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
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
                result["core_lexicon"] = {
                    "total_entries": len(lexicon_dict),
                    "categories": categories,
                    "compact_id_count": len(compact_ids),
                    "compact_id_min": min(compact_ids) if compact_ids else None,
                    "compact_id_max": max(compact_ids) if compact_ids else None
                }
        else:
            result["core_lexicon"] = {"error": "core_lexicon.json not found"}
            
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                result["macro_lexicon"] = {
                    "total_entries": len(macro_data) if isinstance(macro_data, (dict, list)) else 0
                }
        else:
            result["macro_lexicon"] = {"error": "macro_lexicon.json not found"}
            
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicons()
