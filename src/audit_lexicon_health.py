import sys
import os
import json
import traceback

def audit_lexicons():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    if not workspace.endswith('/'):
        workspace += '/'
    
    lexicon_dir = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon')
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
                "status": "success",
                "total_entries": len(lexicon_dict),
                "categories": categories,
                "compact_id_count": len(compact_ids)
            }
        except Exception as e:
            result["core_lexicon"] = {"status": "error", "message": str(e)}
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            
            lexicon_dict = macro_data.get('lexicon', macro_data)
            categories = {}
            if isinstance(lexicon_dict, dict):
                for sym, data in lexicon_dict.items():
                    if isinstance(data, dict):
                        cat = data.get('category', 'unknown')
                        categories[cat] = categories.get(cat, 0) + 1
                        
            result["macro_lexicon"] = {
                "status": "success",
                "total_entries": len(lexicon_dict) if isinstance(lexicon_dict, dict) else 0,
                "categories": categories
            }
        except Exception as e:
            result["macro_lexicon"] = {"status": "error", "message": str(e)}
            
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    audit_lexicons()
