import sys
import os
import json
import traceback

def audit_lexicon():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    result = {
        "core_lexicon_status": "missing",
        "macro_lexicon_status": "missing",
        "core_categories": {},
        "macro_categories": {},
        "core_total_entries": 0,
        "macro_total_entries": 0
    }
    
    try:
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                result["core_lexicon_status"] = "loaded"
                lexicon_dict = core_data.get("lexicon", {})
                result["core_total_entries"] = len(lexicon_dict)
                categories = {}
                for sym, data in lexicon_dict.items():
                    cat = data.get("category", "unknown") if isinstance(data, dict) else "unknown"
                    categories[cat] = categories.get(cat, 0) + 1
                result["core_categories"] = categories
        else:
            result["core_lexicon_status"] = "not_found"
            
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                result["macro_lexicon_status"] = "loaded"
                macro_dict = macro_data.get("lexicon", macro_data)
                if isinstance(macro_dict, dict):
                    result["macro_total_entries"] = len(macro_dict)
                    categories = {}
                    for sym, data in macro_dict.items():
                        cat = data.get("category", "unknown") if isinstance(data, dict) else "unknown"
                        categories[cat] = categories.get(cat, 0) + 1
                    result["macro_categories"] = categories
        else:
            result["macro_lexicon_status"] = "not_found"
            
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"Error during audit: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    audit_lexicon()
