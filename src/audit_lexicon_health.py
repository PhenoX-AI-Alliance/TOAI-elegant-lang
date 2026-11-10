import sys
import os
import json
import traceback

def audit_lexicon():
    base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(base_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "core_stats": {},
        "macro_stats": {},
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
                report["core_stats"]["total_symbols"] = len(lexicon_map)
                report["core_stats"]["category_distribution"] = categories
                report["core_stats"]["compact_id_count"] = len(compact_ids)
        else:
            report["core_stats"]["error"] = "core_lexicon.json not found"
            
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                report["macro_stats"]["total_macros"] = len(macro_data)
        else:
            report["macro_stats"]["error"] = "macro_lexicon.json not found"
            
        print(json.dumps(report, ensure_ascii=False, indent=2))
        
    except Exception as e:
        error_report = {
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }
        print(json.dumps(error_report, ensure_ascii=False, indent=2))
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicon()
