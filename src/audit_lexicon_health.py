import sys
import os
import json

def audit_lexicons():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lex_dir = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lex_dir, 'core_lexicon.json')
    macro_path = os.path.join(lex_dir, 'macro_lexicon.json')
    
    result = {
        "core_lexicon_status": "missing",
        "macro_lexicon_status": "missing",
        "core_categories": {},
        "macro_categories": {},
        "core_count": 0,
        "macro_count": 0
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lexicon = core_data.get('lexicon', {})
                result["core_count"] = len(lexicon)
                result["core_lexicon_status"] = "loaded"
                
                cats = {}
                for sym, data in lexicon.items():
                    cat = data.get('category', 'unknown')
                    cats[cat] = cats.get(cat, 0) + 1
                result["core_categories"] = cats
        except Exception as e:
            result["core_lexicon_status"] = f"error: {str(e)}"
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                lexicon = macro_data.get('lexicon', macro_data)
                if isinstance(lexicon, dict):
                    result["macro_count"] = len(lexicon)
                    result["macro_lexicon_status"] = "loaded"
                    cats = {}
                    for sym, data in lexicon.items():
                        if isinstance(data, dict):
                            cat = data.get('category', 'unknown')
                            cats[cat] = cats.get(cat, 0) + 1
                    result["macro_categories"] = cats
                else:
                    result["macro_lexicon_status"] = "invalid format"
        except Exception as e:
            result["macro_lexicon_status"] = f"error: {str(e)}"
            
    output_path = os.path.join(workspace, 'TOAI_Generated', 'lexicon_audit_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    audit_lexicons()
