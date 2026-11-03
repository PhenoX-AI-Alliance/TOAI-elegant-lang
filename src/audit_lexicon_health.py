import sys
import os
import traceback
import json

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "core_lexicon_status": "missing",
        "macro_lexicon_status": "missing",
        "core_categories": {},
        "macro_categories": {},
        "total_core_symbols": 0,
        "total_macro_symbols": 0
    }
    
    try:
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lexicon_map = core_data.get('lexicon', {})
                report["total_core_symbols"] = len(lexicon_map)
                cats = {}
                for sym, data in lexicon_map.items():
                    cat = data.get('category', 'unknown')
                    cats[cat] = cats.get(cat, 0) + 1
                report["core_categories"] = cats
                report["core_lexicon_status"] = "loaded"
        
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                macro_map = macro_data.get('lexicon', {})
                report["total_macro_symbols"] = len(macro_map)
                m_cats = {}
                for sym, data in macro_map.items():
                    cat = data.get('category', 'unknown')
                    m_cats[cat] = m_cats.get(cat, 0) + 1
                report["macro_categories"] = m_cats
                report["macro_lexicon_status"] = "loaded"
                
        print(json.dumps(report, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"Error during audit: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicons()
