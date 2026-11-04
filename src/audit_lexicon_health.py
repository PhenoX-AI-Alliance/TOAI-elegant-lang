import sys
import os
import traceback
import time
import json

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    audit_results = {
        "timestamp": time.time(),
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
                audit_results["core_lexicon"] = {
                    "total_entries": len(lexicon_map),
                    "categories": categories,
                    "compact_id_count": len(compact_ids),
                    "status": "success"
                }
        else:
            audit_results["core_lexicon"] = {"status": "not_found"}
            
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                macro_map = macro_data.get('lexicon', {})
                macro_categories = {}
                for sym, data in macro_map.items():
                    cat = data.get('category', 'unknown')
                    macro_categories[cat] = macro_categories.get(cat, 0) + 1
                audit_results["macro_lexicon"] = {
                    "total_entries": len(macro_map),
                    "categories": macro_categories,
                    "status": "success"
                }
        else:
            audit_results["macro_lexicon"] = {"status": "not_found"}
            
        print(json.dumps(audit_results, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"Error during lexicon audit: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicons()
