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
        "timestamp": os.path.getmtime(core_path) if os.path.exists(core_path) else 0,
        "core_lexicon": {"total_symbols": 0, "categories": {}, "compact_ids": []},
        "macro_lexicon": {"total_symbols": 0, "categories": {}, "compact_ids": []}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lex_dict = core_data.get('lexicon', {})
                report["core_lexicon"]["total_symbols"] = len(lex_dict)
                cats = {}
                cids = []
                for sym, val in lex_dict.items():
                    cat = val.get('category', 'unknown')
                    cats[cat] = cats.get(cat, 0) + 1
                    if 'compact_id' in val:
                        cids.append(val['compact_id'])
                report["core_lexicon"]["categories"] = cats
                report["core_lexicon"]["compact_ids_count"] = len(cids)
        except Exception as e:
            report["core_lexicon"]["error"] = str(e)
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                lex_dict = macro_data.get('lexicon', {})
                report["macro_lexicon"]["total_symbols"] = len(lex_dict)
                cats = {}
                cids = []
                for sym, val in lex_dict.items():
                    cat = val.get('category', 'unknown')
                    cats[cat] = cats.get(cat, 0) + 1
                    if 'compact_id' in val:
                        cids.append(val['compact_id'])
                report["macro_lexicon"]["categories"] = cats
                report["macro_lexicon"]["compact_ids_count"] = len(cids)
        except Exception as e:
            report["macro_lexicon"]["error"] = str(e)
            
    print(json.dumps(report, ensure_ascii=False, indent=2))
    
    output_report_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon', 'audit_report.json')
    with open(output_report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    audit_lexicons()
