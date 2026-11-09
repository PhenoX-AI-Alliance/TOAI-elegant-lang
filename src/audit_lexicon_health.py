import sys
import os
import json
import traceback

def audit_lexicon():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
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
                report["core_count"] = len(lexicon)
                report["core_lexicon_status"] = "loaded"
                
                cats = {}
                for sym, data in lexicon.items():
                    cat = data.get('category', 'unknown') if isinstance(data, dict) else 'unknown'
                    cats[cat] = cats.get(cat, 0) + 1
                report["core_categories"] = cats
        except Exception as e:
            report["core_lexicon_status"] = f"error: {str(e)}"
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                if isinstance(macro_data, dict):
                    report["macro_count"] = len(macro_data)
                    report["macro_lexicon_status"] = "loaded"
                    cats = {}
                    for sym, data in macro_data.items():
                        cat = data.get('category', 'unknown') if isinstance(data, dict) else 'unknown'
                        cats[cat] = cats.get(cat, 0) + 1
                    report["macro_categories"] = cats
                elif isinstance(macro_data, list):
                    report["macro_count"] = len(macro_data)
                    report["macro_lexicon_status"] = "loaded_list"
        except Exception as e:
            report["macro_lexicon_status"] = f"error: {str(e)}"
            
    output_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon_audit_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        audit_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
