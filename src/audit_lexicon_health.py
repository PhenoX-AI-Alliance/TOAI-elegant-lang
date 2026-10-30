import sys
import os
import json
import traceback

def audit_lexicon():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    elegant_lang_dir = os.path.join(workspace, 'TOAI-elegant-lang')
    lexicon_dir = os.path.join(elegant_lang_dir, 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "status": "success",
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
                        if 'compact_id' in data:
                            compact_ids.append(data['compact_id'])
                report['core_lexicon'] = {
                    "total_symbols": len(lexicon_dict),
                    "category_distribution": categories,
                    "compact_id_count": len(compact_ids)
                }
        else:
            report['core_lexicon'] = {"error": "core_lexicon.json not found"}
            
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                report['macro_lexicon'] = {
                    "total_macros": len(macro_data) if isinstance(macro_data, (dict, list)) else 0
                }
        else:
            report['macro_lexicon'] = {"error": "macro_lexicon.json not found"}
            
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
