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
        "core_lexicon": {"total_symbols": 0, "categories": {}, "compact_ids": []},
        "macro_lexicon": {"total_symbols": 0, "categories": {}, "compact_ids": []}
    }
    
    try:
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lexicon_map = core_data.get('lexicon', {})
                results["core_lexicon"]["total_symbols"] = len(lexicon_map)
                for sym, data in lexicon_map.items():
                    cat = data.get('category', 'unknown')
                    results["core_lexicon"]["categories"][cat] = results["core_lexicon"]["categories"].get(cat, 0) + 1
                    if 'compact_id' in data:
                        results["core_lexicon"]["compact_ids"].append(data['compact_id'])
                        
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                lexicon_map = macro_data.get('lexicon', {})
                results["macro_lexicon"]["total_symbols"] = len(lexicon_map)
                for sym, data in lexicon_map.items():
                    cat = data.get('category', 'unknown')
                    results["macro_lexicon"]["categories"][cat] = results["macro_lexicon"]["categories"].get(cat, 0) + 1
                    if 'compact_id' in data:
                        results["macro_lexicon"]["compact_ids"].append(data['compact_id'])
                        
        print(json.dumps(results, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error during audit: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicons()
