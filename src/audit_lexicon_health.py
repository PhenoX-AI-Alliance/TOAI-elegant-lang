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
        "core_lexicon": {"status": "missing", "categories": {}, "total_entries": 0},
        "macro_lexicon": {"status": "missing", "total_entries": 0}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            lexicon_dict = core_data.get('lexicon', {})
            categories = {}
            total = len(lexicon_dict)
            for sym, data in lexicon_dict.items():
                cat = data.get('category', 'unknown')
                categories[cat] = categories.get(cat, 0) + 1
            result["core_lexicon"] = {
                "status": "ok",
                "categories": categories,
                "total_entries": total
            }
        except Exception as e:
            result["core_lexicon"]["status"] = f"error: {str(e)}"
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            if isinstance(macro_data, dict):
                total_macro = len(macro_data.get('macros', macro_data))
            elif isinstance(macro_data, list):
                total_macro = len(macro_data)
            else:
                total_macro = 0
            result["macro_lexicon"] = {
                "status": "ok",
                "total_entries": total_macro
            }
        except Exception as e:
            result["macro_lexicon"]["status"] = f"error: {str(e)}"
            
    output_report_path = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon_audit_report.json')
    os.makedirs(os.path.dirname(output_report_path), exist_ok=True)
    with open(output_report_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
        
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    try:
        audit_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)