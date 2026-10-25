import sys
import os
import json
import traceback

def audit_lexicons(base_path):
    core_path = os.path.join(base_path, 'lexicon', 'core_lexicon.json')
    macro_path = os.path.join(base_path, 'lexicon', 'macro_lexicon.json')
    
    report = {
        "core_lexicon": {"status": "missing", "categories": {}, "total": 0},
        "macro_lexicon": {"status": "missing", "total": 0}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            lexicon_dict = core_data.get('lexicon', {})
            categories = {}
            total = len(lexicon_dict)
            
            for sym, data in lexicon_dict.items():
                cat = data.get('category', 'unknown')
                categories[cat] = categories.get(cat, 0) + 1
                
            report["core_lexicon"] = {
                "status": "success",
                "categories": categories,
                "total": total
            }
        except Exception as e:
            report["core_lexicon"] = {
                "status": "error",
                "message": str(e)
            }
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            report["macro_lexicon"] = {
                "status": "success",
                "total": len(macro_data) if isinstance(macro_data, (dict, list)) else 0
            }
        except Exception as e:
            report["macro_lexicon"] = {
                "status": "error",
                "message": str(e)
            }
            
    return report

def main():
    base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    target_dir = os.path.join(base_dir, 'TOAI_Generated')
    os.makedirs(target_dir, exist_ok=True)
    
    audit_results = audit_lexicons(base_dir)
    
    output_path = os.path.join(target_dir, 'lexicon_audit_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(audit_results, f, ensure_ascii=False, indent=2)
        
    print(f"Audit completed. Report saved to {output_path}")

if __name__ == '__main__':
    main()
