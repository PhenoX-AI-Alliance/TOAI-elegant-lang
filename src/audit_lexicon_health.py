import sys
import os
import json
import traceback

def audit_lexicon():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "core_status": "missing",
        "macro_status": "missing",
        "core_categories": {},
        "macro_categories": {},
        "core_count": 0,
        "macro_count": 0,
        "errors": []
    }
    
    try:
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lexicon_dict = core_data.get('lexicon', {})
                report["core_count"] = len(lexicon_dict)
                report["core_status"] = "loaded"
                
                categories = {}
                for sym, data in lexicon_dict.items():
                    cat = data.get('category', 'unknown') if isinstance(data, dict) else 'unknown'
                    categories[cat] = categories.get(cat, 0) + 1
                report["core_categories"] = categories
        else:
            report["errors"].append(f"Core lexicon not found at {core_path}")
            
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                macro_dict = macro_data.get('lexicon', macro_data)
                if isinstance(macro_dict, dict):
                    report["macro_count"] = len(macro_dict)
                    report["macro_status"] = "loaded"
                    
                    macro_cats = {}
                    for sym, data in macro_dict.items():
                        cat = data.get('category', 'unknown') if isinstance(data, dict) else 'unknown'
                        macro_cats[cat] = macro_cats.get(cat, 0) + 1
                    report["macro_categories"] = macro_cats
                else:
                    report["macro_status"] = "invalid_format"
        else:
            report["errors"].append(f"Macro lexicon not found at {macro_path}")
            
        print(json.dumps(report, ensure_ascii=False, indent=2))
        
    except Exception as e:
        error_info = {
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }
        print(json.dumps(error_info, ensure_ascii=False, indent=2))
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicon()
