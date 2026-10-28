import sys
import os
import json
import traceback

def audit_lexicon():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '.')
    base_lexicon_dir = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(base_lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(base_lexicon_dir, 'macro_lexicon.json')
    
    result = {
        "core_lexicon": {},
        "macro_lexicon": {},
        "status": "success"
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
                        if 'compact_id' in data:
                            compact_ids.append(data['compact_id'])
                result["core_lexicon"] = {
                    "total_symbols": len(lexicon_dict),
                    "category_distribution": categories,
                    "compact_id_count": len(compact_ids)
                }
        else:
            result["core_lexicon"] = {"error": "core_lexicon.json not found"}
            
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                result["macro_lexicon"] = {
                    "total_entries": len(macro_data) if isinstance(macro_data, dict) else 0
                }
        else:
            result["macro_lexicon"] = {"error": "macro_lexicon.json not found"}
            
    except Exception as e:
        result["status"] = "error"
        result["message"] = str(e)
        
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    audit_lexicon()
