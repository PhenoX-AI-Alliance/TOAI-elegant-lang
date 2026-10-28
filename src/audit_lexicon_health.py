import sys
import os
import traceback
import time
import json

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    result = {
        "timestamp": time.time(),
        "core_lexicon": {"status": "missing", "stats": {}},
        "macro_lexicon": {"status": "missing", "stats": {}}
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
                        
            result["core_lexicon"] = {
                "status": "loaded",
                "total_symbols": len(lexicon_map),
                "categories": categories,
                "compact_id_count": len(compact_ids)
            }
        except Exception as e:
            result["core_lexicon"] = {"status": "error", "message": str(e)}
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            result["macro_lexicon"] = {
                "status": "loaded",
                "total_macros": len(macro_data) if isinstance(macro_data, dict) else 0
            }
        except Exception as e:
            result["macro_lexicon"] = {"status": "error", "message": str(e)}
            
    output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'lexicon_audit_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
        
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    try:
        audit_lexicons()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
