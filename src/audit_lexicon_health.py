import sys
import os
import json
import traceback

def audit_lexicons():
    try:
        base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        lang_dir = os.path.join(base_dir, 'TOAI-elegant-lang')
        lexicon_dir = os.path.join(lang_dir, 'lexicon')
        
        core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
        macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
        
        report = {
            "core_lexicon": {"status": "missing", "categories": {}, "total": 0},
            "macro_lexicon": {"status": "missing", "categories": {}, "total": 0}
        }
        
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            lexicon_dict = core_data.get('lexicon', {})
            categories = {}
            for sym, data in lexicon_dict.items():
                cat = data.get('category', 'unknown')
                categories[cat] = categories.get(cat, 0) + 1
            report["core_lexicon"] = {
                "status": "ok",
                "categories": categories,
                "total": len(lexicon_dict)
            }
            
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            if isinstance(macro_data, dict):
                m_items = macro_data.get('macros', macro_data)
                report["macro_lexicon"] = {
                    "status": "ok",
                    "total": len(m_items)
                }
                
        output_path = os.path.join(lang_dir, 'lexicon_health_report.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        print(f"Audit completed successfully. Report saved to {output_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicons()
