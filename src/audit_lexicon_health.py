# -*- coding: utf-8 -*-
import sys
import os
import json
import traceback

def audit_lexicons():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lex_dir = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lex_dir, 'core_lexicon.json')
    macro_path = os.path.join(lex_dir, 'macro_lexicon.json')
    
    results = {
        "core_lexicon_status": "missing",
        "macro_lexicon_status": "missing",
        "core_categories": {},
        "macro_categories": {},
        "core_count": 0,
        "macro_count": 0
    }
    
    try:
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            lexicon_dict = core_data.get('lexicon', {})
            results["core_count"] = len(lexicon_dict)
            results["core_lexicon_status"] = "loaded"
            
            cats = {}
            for sym, data in lexicon_dict.items():
                cat = data.get('category', 'unknown') if isinstance(data, dict) else 'unknown'
                cats[cat] = cats.get(cat, 0) + 1
            results["core_categories"] = cats
        
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            macro_dict = macro_data.get('lexicon', {}) if isinstance(macro_data, dict) and 'lexicon' in macro_data else macro_data
            if isinstance(macro_dict, dict):
                results["macro_count"] = len(macro_dict)
                results["macro_lexicon_status"] = "loaded"
                mcats = {}
                for sym, data in macro_dict.items():
                    cat = data.get('category', 'unknown') if isinstance(data, dict) else 'unknown'
                    mcats[cat] = mcats.get(cat, 0) + 1
                results["macro_categories"] = mcats
                
        print(json.dumps(results, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"Error during audit: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicons()
