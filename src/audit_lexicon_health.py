import sys
import os
import json
import traceback

def audit_lexicon():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    result = {
        "status": "success",
        "core_lexicon": {},
        "macro_lexicon": {}
    }
    
    try:
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lexicon_map = core_data.get('lexicon', {})
                categories = {}
                compact_ids = []
                for sym, data in lexicon_map.items():
                    cat = data.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    if 'compact_id' in data:
                        compact_ids.append(data['compact_id'])
                result['core_lexicon'] = {
                    "total_symbols": len(lexicon_map),
                    "categories": categories,
                    "compact_id_count": len(compact_ids)
                }
        else:
            result['core_lexicon'] = {"error": "core_lexicon.json not found"}
            
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                result['macro_lexicon'] = {
                    "total_macros": len(macro_data) if isinstance(macro_data, dict) else 0
                }
        else:
            result['macro_lexicon'] = {"error": "macro_lexicon.json not found"}
            
    except Exception as e:
        result['status'] = "error"
        result['message'] = str(e)
        result['traceback'] = traceback.format_exc()
        
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    audit_lexicon()
