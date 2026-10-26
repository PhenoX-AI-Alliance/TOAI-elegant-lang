import sys
import os
import json
import traceback

def audit_lexicons():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace, 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "core_lexicon": {"exists": False, "categories": {}, "total_symbols": 0},
        "macro_lexicon": {"exists": False, "categories": {}, "total_symbols": 0}
    }
    
    if os.path.exists(core_path):
        report["core_lexicon"]["exists"] = True
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                lexicon_data = data.get('lexicon', {})
                report["core_lexicon"]["total_symbols"] = len(lexicon_data)
                cats = {}
                for sym, val in lexicon_data.items():
                    cat = val.get('category', 'unknown') if isinstance(val, dict) else 'unknown'
                    cats[cat] = cats.get(cat, 0) + 1
                report["core_lexicon"]["categories"] = cats
        except Exception as e:
            report["core_lexicon"]["error"] = str(e)
            
    if os.path.exists(macro_path):
        report["macro_lexicon"]["exists"] = True
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                lexicon_data = data.get('lexicon', data) if isinstance(data, dict) else {}
                report["macro_lexicon"]["total_symbols"] = len(lexicon_data)
                cats = {}
                if isinstance(lexicon_data, dict):
                    for sym, val in lexicon_data.items():
                        cat = val.get('category', 'unknown') if isinstance(val, dict) else 'unknown'
                        cats[cat] = cats.get(cat, 0) + 1
                report["macro_lexicon"]["categories"] = cats
        except Exception as e:
            report["macro_lexicon"]["error"] = str(e)
            
    output_path = os.path.join(workspace, 'TOAI_Generated', 'lexicon_audit_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        audit_lexicons()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)