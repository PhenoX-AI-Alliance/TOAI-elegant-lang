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
        "core_lexicon_status": "missing",
        "macro_lexicon_status": "missing",
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
                report["core_lexicon_status"] = "loaded"
                lexicon_dict = core_data.get('lexicon', {})
                report["core_count"] = len(lexicon_dict)
                for sym, data in lexicon_dict.items():
                    if isinstance(data, dict):
                        cat = data.get('category', 'unknown')
                        report["core_categories"][cat] = report["core_categories"].get(cat, 0) + 1
        else:
            report["errors"].append(f"Core lexicon not found at {core_path}")
            
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                report["macro_lexicon_status"] = "loaded"
                if isinstance(macro_data, dict):
                    report["macro_count"] = len(macro_data)
                    for sym, data in macro_data.items():
                        if isinstance(data, dict):
                            cat = data.get('category', 'unknown')
                            report["macro_categories"][cat] = report["macro_categories"].get(cat, 0) + 1
                elif isinstance(macro_data, list):
                    report["macro_count"] = len(macro_data)
        else:
            report["errors"].append(f"Macro lexicon not found at {macro_path}")
            
    except Exception as e:
        report["errors"].append(str(e))
        
    output_path = os.path.join(elegant_lang_dir, 'lexicon_audit_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    audit_lexicon()
