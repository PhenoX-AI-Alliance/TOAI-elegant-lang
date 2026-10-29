import sys
import os
import json
import traceback

def audit_lexicon():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    result = {
        "core_status": "missing",
        "macro_status": "missing",
        "core_stats": {},
        "macro_stats": {}
    }
    
    try:
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lexicon = core_data.get('lexicon', {})
                categories = {}
                compact_ids = []
                for sym, data in lexicon.items():
                    cat = data.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    if 'compact_id' in data:
                        compact_ids.append(data['compact_id'])
                result["core_status"] = "loaded"
                result["core_stats"] = {
                    "total_symbols": len(lexicon),
                    "categories": categories,
                    "compact_id_count": len(compact_ids)
                }
    except Exception as e:
        result["core_status"] = f"error: {str(e)}"

    try:
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                result["macro_status"] = "loaded"
                result["macro_stats"] = {
                    "total_macros": len(macro_data) if isinstance(macro_data, (list, dict)) else 0
                }
    except Exception as e:
        result["macro_status"] = f"error: {str(e)}"
        
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    audit_lexicon()
