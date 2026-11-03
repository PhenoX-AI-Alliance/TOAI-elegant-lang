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
        "core_lexicon": {"total_symbols": 0, "categories": {}, "compact_id_stats": {}},
        "macro_lexicon": {"total_symbols": 0, "categories": {}, "compact_id_stats": {}}
    }
    
    try:
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                lexicon_map = data.get('lexicon', {})
                report["core_lexicon"]["total_symbols"] = len(lexicon_map)
                cats = {}
                for sym, val in lexicon_map.items():
                    cat = val.get('category', 'unknown') if isinstance(val, dict) else 'unknown'
                    cats[cat] = cats.get(cat, 0) + 1
                report["core_lexicon"]["categories"] = cats
                
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                lexicon_map = data.get('lexicon', {})
                report["macro_lexicon"]["total_symbols"] = len(lexicon_map)
                cats = {}
                for sym, val in lexicon_map.items():
                    cat = val.get('category', 'unknown') if isinstance(val, dict) else 'unknown'
                    cats[cat] = cats.get(cat, 0) + 1
                report["macro_lexicon"]["categories"] = cats
                
        print(json.dumps(report, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error during audit: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicons()
