import os
import sys
import json
import traceback

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "core_lexicon": {"status": "missing", "categories": {}, "total_items": 0},
        "macro_lexicon": {"status": "missing", "categories": {}, "total_items": 0}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            lexicon_dict = core_data.get('lexicon', {})
            categories = {}
            total = len(lexicon_dict)
            for sym, data in lexicon_dict.items():
                cat = data.get('category', 'unknown') if isinstance(data, dict) else 'unknown'
                categories[cat] = categories.get(cat, 0) + 1
            report["core_lexicon"] = {
                "status": "loaded",
                "categories": categories,
                "total_items": total
            }
        except Exception as e:
            report["core_lexicon"]["status"] = f"error: {str(e)}"
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            if isinstance(macro_data, dict):
                total = len(macro_data)
                categories = {}
                for k, v in macro_data.items():
                    cat = v.get('category', 'unknown') if isinstance(v, dict) else 'unknown'
                    categories[cat] = categories.get(cat, 0) + 1
                report["macro_lexicon"] = {
                    "status": "loaded",
                    "categories": categories,
                    "total_items": total
                }
            elif isinstance(macro_data, list):
                report["macro_lexicon"] = {
                    "status": "loaded",
                    "categories": {"list": len(macro_data)},
                    "total_items": len(macro_data)
                }
        except Exception as e:
            report["macro_lexicon"]["status"] = f"error: {str(e)}"
            
    output_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon_audit_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    audit_lexicons()
