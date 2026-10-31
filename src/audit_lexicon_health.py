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
        "core_lexicon": {"total": 0, "categories": {}, "compact_id_stats": {}},
        "macro_lexicon": {"total": 0, "categories": {}, "compact_id_stats": {}}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                data = json.load(f).get('lexicon', {})
                report["core_lexicon"]["total"] = len(data)
                cats = {}
                for sym, val in data.items():
                    cat = val.get('category', 'unknown')
                    cats[cat] = cats.get(cat, 0) + 1
                report["core_lexicon"]["categories"] = cats
        except Exception as e:
            report["core_lexicon"]["error"] = str(e)
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                data = json.load(f).get('lexicon', {})
                report["macro_lexicon"]["total"] = len(data)
                cats = {}
                for sym, val in data.items():
                    cat = val.get('category', 'unknown')
                    cats[cat] = cats.get(cat, 0) + 1
                report["macro_lexicon"]["categories"] = cats
        except Exception as e:
            report["macro_lexicon"]["error"] = str(e)
            
    print(json.dumps(report, ensure_ascii=False, indent=2))
    
    output_report_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon_audit_report.json')
    with open(output_report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    try:
        audit_lexicons()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
