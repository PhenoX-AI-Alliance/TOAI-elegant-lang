import sys
import os
import json
import traceback

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "core_lexicon_status": "missing",
        "macro_lexicon_status": "missing",
        "core_categories": {},
        "macro_categories": {},
        "core_count": 0,
        "macro_count": 0
    }
    
    try:
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                report["core_lexicon_status"] = "loaded"
                lexicon_dict = core_data.get('lexicon', {})
                report["core_count"] = len(lexicon_dict)
                cats = {}
                for sym, data in lexicon_dict.items():
                    cat = data.get('category', 'unknown')
                    cats[cat] = cats.get(cat, 0) + 1
                report["core_categories"] = cats
        else:
            report["core_lexicon_status"] = "not_found"
            
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                report["macro_lexicon_status"] = "loaded"
                if isinstance(macro_data, dict):
                    report["macro_count"] = len(macro_data)
                    macro_cats = {}
                    for k, v in macro_data.items():
                        if isinstance(v, dict):
                            cat = v.get('category', 'unknown')
                            macro_cats[cat] = macro_cats.get(cat, 0) + 1
                    report["macro_categories"] = macro_cats
        else:
            report["macro_path_status"] = "not_found"
            
    except Exception as e:
        report["error"] = str(e)
        report["traceback"] = traceback.format_exc()
        
    output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'lexicon_audit_report.json')
    with open(output_path, 'w', encoding='utf-8') as out:
        json.dump(report, out, ensure_ascii=False, indent=2)
    print(f"Audit report successfully generated at: {output_path}")

if __name__ == '__main__':
    audit_lexicons()
