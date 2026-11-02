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
        "core_lexicon": {"status": "missing", "categories": {}, "total_items": 0},
        "macro_lexicon": {"status": "missing", "total_items": 0}
    }
    
    try:
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            
            lexicon_dict = core_data.get('lexicon', {})
            categories = {}
            total = len(lexicon_dict)
            
            for sym, data in lexicon_dict.items():
                cat = data.get('category', 'unknown')
                categories[cat] = categories.get(cat, 0) + 1
                
            report["core_lexicon"] = {
                "status": "ok",
                "categories": categories,
                "total_items": total
            }
        
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            
            macro_total = len(macro_data) if isinstance(macro_data, (list, dict)) else 0
            report["macro_lexicon"] = {
                "status": "ok",
                "total_items": macro_total
            }
            
        print(json.dumps(report, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"Error during lexicon audit: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicons()
