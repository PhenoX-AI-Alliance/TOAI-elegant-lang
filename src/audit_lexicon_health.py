import sys
import os
import json
import traceback

def audit_lexicons():
    try:
        base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        lang_dir = os.path.join(base_dir, 'TOAI-elegant-lang')
        
        core_path = os.path.join(lang_dir, 'lexicon', 'core_lexicon.json')
        macro_path = os.path.join(lang_dir, 'lexicon', 'macro_lexicon.json')
        
        result = {
            "core_lexicon": {"status": "missing", "total_entries": 0, "categories": {}},
            "macro_lexicon": {"status": "missing", "total_entries": 0, "categories": {}}
        }
        
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            lexicon_dict = core_data.get('lexicon', {})
            categories = {}
            for sym, data in lexicon_dict.items():
                cat = data.get('category', 'unknown')
                categories[cat] = categories.get(cat, 0) + 1
            result["core_lexicon"] = {
                "status": "loaded",
                "total_entries": len(lexicon_dict),
                "categories": categories
            }
            
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            if isinstance(macro_data, dict):
                m_entries = macro_data.get('macros', macro_data)
                result["macro_lexicon"] = {
                    "status": "loaded",
                    "total_entries": len(m_entries) if isinstance(m_entries, (dict, list)) else 0,
                    "categories": {}
                }
                
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"Error during audit: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicons()
