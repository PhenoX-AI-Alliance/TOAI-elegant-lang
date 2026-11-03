import sys
import os
import json
import traceback

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    results = {
        "core_lexicon": {"total": 0, "categories": {}, "compact_ids": []},
        "macro_lexicon": {"total": 0, "categories": {}, "compact_ids": []}
    }
    
    try:
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                lexicon = data.get('lexicon', {})
                results["core_lexicon"]["total"] = len(lexicon)
                for sym, val in lexicon.items():
                    cat = val.get('category', 'unknown')
                    results["core_lexicon"]["categories"][cat] = results["core_lexicon"]["categories"].get(cat, 0) + 1
                    if 'compact_id' in val:
                        results["core_lexicon"]["compact_ids"].append(val['compact_id'])
                        
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                lexicon = data.get('lexicon', {})
                results["macro_lexicon"]["total"] = len(lexicon)
                for sym, val in lexicon.items():
                    cat = val.get('category', 'unknown')
                    results["macro_lexicon"]["categories"][cat] = results["macro_lexicon"]["categories"].get(cat, 0) + 1
                    if 'compact_id' in val:
                        results["macro_lexicon"]["compact_ids"].append(val['compact_id'])
                        
        print(json.dumps(results, ensure_ascii=False, indent=2))
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicons()
