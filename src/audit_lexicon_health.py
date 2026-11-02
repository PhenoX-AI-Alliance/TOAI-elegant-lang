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
        "core_lexicon": {"categories": {}, "compact_ids": []},
        "macro_lexicon": {"categories": {}, "compact_ids": []}
    }
    
    if os.path.exists(core_path):
        with open(core_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            lex_dict = data.get('lexicon', {})
            for sym, val in lex_dict.items():
                cat = val.get('category', 'unknown')
                report["core_lexicon"]["categories"][cat] = report["core_lexicon"]["categories"].get(cat, 0) + 1
                if 'compact_id' in val:
                    report["core_lexicon"]["compact_ids"].append(val['compact_id'])
                    
    if os.path.exists(macro_path):
        with open(macro_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            macro_dict = data.get('macro_lexicon', data.get('lexicon', {}))
            for sym, val in macro_dict.items():
                cat = val.get('category', 'unknown')
                report["macro_lexicon"]["categories"][cat] = report["macro_lexicon"]["categories"].get(cat, 0) + 1
                if 'compact_id' in val:
                    report["macro_lexicon"]["compact_ids"].append(val['compact_id'])
                    
    output_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon', 'audit_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        audit_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
