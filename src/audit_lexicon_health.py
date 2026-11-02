import sys
import os
import json
import traceback

def audit_lexicons():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "core_lexicon_exists": os.path.exists(core_path),
        "macro_lexicon_exists": os.path.exists(macro_path),
        "core_categories": {},
        "macro_categories": {},
        "core_count": 0,
        "macro_count": 0
    }
    
    if report["core_lexicon_exists"]:
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lexicon_dict = core_data.get('lexicon', {})
                report["core_count"] = len(lexicon_dict)
                for sym, val in lexicon_dict.items():
                    cat = val.get('category', 'unknown') if isinstance(val, dict) else 'unknown'
                    report["core_categories"][cat] = report["core_categories"].get(cat, 0) + 1
        except Exception as e:
            report["core_error"] = str(e)
            
    if report["macro_lexicon_exists"]:
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                if isinstance(macro_data, dict):
                    report["macro_count"] = len(macro_data)
                    for sym, val in macro_data.items():
                        cat = val.get('category', 'unknown') if isinstance(val, dict) else 'unknown'
                        report["macro_categories"][cat] = report["macro_categories"].get(cat, 0) + 1
                elif isinstance(macro_data, list):
                    report["macro_count"] = len(macro_data)
        except Exception as e:
            report["macro_error"] = str(e)
            
    output_path = os.path.join(lexicon_dir, 'audit_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"Audit report successfully generated at: {output_path}")

if __name__ == '__main__':
    audit_lexicons()
