import sys
import os
import json
import traceback

def audit_lexicons():
    base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(base_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "core_lexicon": {"status": "missing", "category_distribution": {}, "total_symbols": 0},
        "macro_lexicon": {"status": "missing", "category_distribution": {}, "total_symbols": 0}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            lexicon = core_data.get('lexicon', {})
            categories = {}
            for sym, data in lexicon.items():
                cat = data.get('category', 'unknown')
                categories[cat] = categories.get(cat, 0) + 1
            report["core_lexicon"] = {
                "status": "success",
                "category_distribution": categories,
                "total_symbols": len(lexicon)
            }
        except Exception as e:
            report["core_lexicon"]["status"] = f"error: {str(e)}"
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            lexicon = macro_data.get('lexicon', macro_data)
            if isinstance(lexicon, dict):
                categories = {}
                for sym, data in lexicon.items():
                    if isinstance(data, dict):
                        cat = data.get('category', 'unknown')
                    else:
                        cat = 'unknown'
                    categories[cat] = categories.get(cat, 0) + 1
                report["macro_lexicon"] = {
                    "status": "success",
                    "category_distribution": categories,
                    "total_symbols": len(lexicon)
                }
            else:
                report["macro_lexicon"]["status"] = "invalid_format"
        except Exception as e:
            report["macro_lexicon"]["status"] = f"error: {str(e)}"
            
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    audit_lexicons()
