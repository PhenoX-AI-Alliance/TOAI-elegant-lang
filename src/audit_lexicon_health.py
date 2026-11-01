import sys
import os
import json
import traceback

def audit_lexicon():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "timestamp": os.path.getmtime(core_path) if os.path.exists(core_path) else 0,
        "core_lexicon": {"exists": False, "categories": {}, "total_items": 0},
        "macro_lexicon": {"exists": False, "total_items": 0}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lexicon_dict = core_data.get('lexicon', {})
                report["core_lexicon"]["exists"] = True
                report["core_lexicon"]["total_items"] = len(lexicon_dict)
                
                categories = {}
                for sym, data in lexicon_dict.items():
                    if isinstance(data, dict):
                        cat = data.get('category', 'unknown')
                        categories[cat] = categories.get(cat, 0) + 1
                report["core_lexicon"]["categories"] = categories
        except Exception as e:
            report["core_lexicon"]["error"] = str(e)
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                report["macro_lexicon"]["exists"] = True
                if isinstance(macro_data, dict):
                    report["macro_lexicon"]["total_items"] = len(macro_data)
                elif isinstance(macro_data, list):
                    report["macro_lexicon"]["total_items"] = len(macro_data)
        except Exception as e:
            report["macro_lexicon"]["error"] = str(e)
            
    output_report_path = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon_audit_report.json')
    with open(output_report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"Audit completed successfully. Report saved to {output_report_path}")

if __name__ == '__main__':
    try:
        audit_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
