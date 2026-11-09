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
        "core_lexicon": {"status": "missing", "categories": {}, "compact_id_stats": {}},
        "macro_lexicon": {"status": "missing", "categories": {}, "compact_id_stats": {}}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            lexicon_map = core_data.get('lexicon', {})
            categories = {}
            compact_ids = []
            
            for sym, data in lexicon_map.items():
                if isinstance(data, dict):
                    cat = data.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    if 'compact_id' in data:
                        compact_ids.append(data['compact_id'])
                        
            result["core_lexicon"]["status"] = "success"
            result["core_lexicon"]["total_entries"] = len(lexicon_map)
            result["core_lexicon"]["categories"] = categories
            result["core_lexicon"]["compact_id_stats"] = {
                "count": len(compact_ids),
                "min": min(compact_ids) if compact_ids else None,
                "max": max(compact_ids) if compact_ids else None
            }
        except Exception as e:
            result["core_lexicon"]["status"] = "error"
            result["core_lexicon"]["message"] = str(e)
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            lexicon_map = macro_data.get('lexicon', {}) if isinstance(macro_data, dict) else {}
            if not lexicon_map and isinstance(macro_data, dict):
                lexicon_map = macro_data
                
            categories = {}
            compact_ids = []
            
            for sym, data in lexicon_map.items():
                if isinstance(data, dict):
                    cat = data.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    if 'compact_id' in data:
                        compact_ids.append(data['compact_id'])
                        
            result["macro_lexicon"]["status"] = "success"
            result["macro_lexicon"]["total_entries"] = len(lexicon_map)
            result["macro_lexicon"]["categories"] = categories
            result["macro_lexicon"]["compact_id_stats"] = {
                "count": len(compact_ids),
                "min": min(compact_ids) if compact_ids else None,
                "max": max(compact_ids) if compact_ids else None
            }
        except Exception as e:
            result["macro_lexicon"]["status"] = "error"
            result["macro_lexicon"]["message"] = str(e)
            
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        audit_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
