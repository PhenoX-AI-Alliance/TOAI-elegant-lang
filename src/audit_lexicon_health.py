import sys
import os
import json
import traceback

def audit_lexicons():
    try:
        base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        lexicon_dir = os.path.join(base_dir, 'TOAI-elegant-lang', 'lexicon')
        
        core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
        macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
        
        report = {
            "core_lexicon": {"status": "missing", "categories": {}, "total_items": 0},
            "macro_lexicon": {"status": "missing", "total_items": 0}
        }
        
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lexicon_dict = core_data.get('lexicon', {})
                report["core_lexicon"]["status"] = "loaded"
                report["core_lexicon"]["total_items"] = len(lexicon_dict)
                
                cats = {}
                for sym, data in lexicon_dict.items():
                    cat = data.get('category', 'unknown')
                    cats[cat] = cats.get(cat, 0) + 1
                report["core_lexicon"]["categories"] = cats
        
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                report["macro_lexicon"]["status"] = "loaded"
                if isinstance(macro_data, dict):
                    report["macro_lexicon"]["total_items"] = len(macro_data)
                elif isinstance(macro_data, list):
                    report["macro_lexicon"]["total_items"] = len(macro_data)
                    
        print(json.dumps(report, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"Error during audit: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicons()
