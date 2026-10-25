import sys
import os
import json
import traceback

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    audit_result = {
        "core_lexicon": {},
        "macro_lexicon": {},
        "status": "success"
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
                audit_result["core_lexicon"] = {
                    "total_symbols": len(lexicon_map),
                    "category_distribution": categories,
                    "compact_id_count": len(compact_ids)
                }
        else:
            audit_result["core_lexicon"] = {"error": "core_lexicon.json not found"}
            
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                audit_result["macro_lexicon"] = {
                    "total_macros": len(macro_data) if isinstance(macro_data, dict) else 0
                }
        else:
            audit_result["macro_lexicon"] = {"error": "macro_lexicon.json not found"}
            
        print(json.dumps(audit_result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        error_output = {
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }
        print(json.dumps(error_output, ensure_ascii=False, indent=2))
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicons()
