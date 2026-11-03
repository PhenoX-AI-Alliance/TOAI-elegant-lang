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
        "core_lexicon": {"exists": False, "categories": {}, "total_items": 0},
        "macro_lexicon": {"exists": False, "categories": {}, "total_items": 0}
    }
    
    try:
        if os.path.exists(core_path):
            report["core_lexicon"]["exists"] = True
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lexicon_map = core_data.get('lexicon', {})
                report["core_lexicon"]["total_items"] = len(lexicon_map)
                
                categories = {}
                for sym, data in lexicon_map.items():
                    cat = data.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                report["core_lexicon"]["categories"] = categories
        
        if os.path.exists(macro_path):
            report["macro_lexicon"]["exists"] = True
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                if isinstance(macro_data, dict):
                    macro_map = macro_data.get('lexicon', macro_data)
                    report["macro_lexicon"]["total_items"] = len(macro_map)
                    categories = {}
                    for sym, data in macro_map.items():
                        if isinstance(data, dict):
                            cat = data.get('category', 'macro')
                        else:
                            cat = 'macro'
                        categories[cat] = categories.get(cat, 0) + 1
                    report["macro_lexicon"]["categories"] = categories
                    
        print(json.dumps(report, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"Error during audit: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicons()
