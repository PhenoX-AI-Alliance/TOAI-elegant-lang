import sys
import os
import json
import traceback

def audit_lexicons():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    audit_results = {
        "timestamp": os.path.exists(core_path) and os.path.getmtime(core_path) or 0,
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
                audit_results["core_count"] = len(lexicon_dict)
                audit_results["core_lexicon_status"] = "loaded"
                
                cats = {}
                for sym, data in lexicon_dict.items():
                    cat = data.get('category', 'unknown') if isinstance(data, dict) else 'unknown'
                    cats[cat] = cats.get(cat, 0) + 1
                audit_results["core_categories"] = cats
        else:
            audit_results["core_lexicon_status"] = "file_not_found"
            
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                if isinstance(macro_data, dict):
                    audit_results["macro_count"] = len(macro_data)
                    audit_results["macro_lexicon_status"] = "loaded"
                    mcats = {}
                    for k, v in macro_data.items():
                        cat = v.get('category', 'unknown') if isinstance(v, dict) else 'unknown'
                        mcats[cat] = mcats.get(cat, 0) + 1
                    audit_results["macro_categories"] = mcats
                else:
                    audit_results["macro_lexicon_status"] = "invalid_format"
        else:
            audit_results["macro_lexicon_status"] = "file_not_found"
            
        print(json.dumps(audit_results, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"Error during lexicon audit: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    audit_lexicons()
