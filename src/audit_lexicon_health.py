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
        "timestamp": os.path.getmtime(core_path) if os.path.exists(core_path) else 0,
        "core_lexicon": {"status": "missing", "categories": {}, "total_items": 0},
        "macro_lexicon": {"status": "missing", "categories": {}, "total_items": 0}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                lexicon_map = data.get('lexicon', {})
                categories = {}
                for sym, val in lexicon_map.items():
                    cat = val.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                report['core_lexicon'] = {
                    "status": "ok",
                    "categories": categories,
                    "total_items": len(lexicon_map)
                }
        except Exception as e:
            report['core_lexicon']['status'] = f"error: {str(e)}"
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                macros_map = data.get('macros', data.get('lexicon', {}))
                categories = {}
                for sym, val in macros_map.items():
                    cat = val.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                report['macro_lexicon'] = {
                    "status": "ok",
                    "categories": categories,
                    "total_items": len(macros_map)
                }
        except Exception as e:
            report['macro_lexicon']['status'] = f"error: {str(e)}"
            
    output_path = os.path.join(lexicon_dir, 'lexicon_audit_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    audit_lexicons()
