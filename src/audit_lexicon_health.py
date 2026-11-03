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
        "timestamp": os.path.exists(core_path) and os.path.getmtime(core_path) or 0,
        "core_lexicon": {},
        "macro_lexicon": {}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                lex = data.get('lexicon', {})
                categories = {}
                compact_ids = []
                for sym, val in lex.items():
                    cat = val.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    if 'compact_id' in val:
                        compact_ids.append(val['compact_id'])
                report["core_lexicon"] = {
                    "total_symbols": len(lex),
                    "categories": categories,
                    "compact_id_count": len(compact_ids)
                }
        except Exception as e:
            report["core_lexicon"]["error"] = str(e)
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                lex = data.get('lexicon', {})
                categories = {}
                compact_ids = []
                for sym, val in lex.items():
                    cat = val.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    if 'compact_id' in val:
                        compact_ids.append(val['compact_id'])
                report["macro_lexicon"] = {
                    "total_symbols": len(lex),
                    "categories": categories,
                    "compact_id_count": len(compact_ids)
                }
        except Exception as e:
            report["macro_lexicon"]["error"] = str(e)
            
    output_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon', 'audit_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"Audit completed. Report saved to {output_path}")

if __name__ == '__main__':
    try:
        audit_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
