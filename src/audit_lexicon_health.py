import sys
import os
import json
import traceback

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "core_lexicon_status": "missing",
        "macro_lexicon_status": "missing",
        "core_categories": {},
        "macro_categories": {},
        "core_total": 0,
        "macro_total": 0
    }
    
    try:
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lexicon_map = core_data.get('lexicon', {})
                report["core_lexicon_status"] = "loaded"
                report["core_total"] = len(lexicon_map)
                
                categories = {}
                for sym, data in lexicon_map.items():
                    cat = data.get('category', 'unknown') if isinstance(data, dict) else 'unknown'
                    categories[cat] = categories.get(cat, 0) + 1
                report["core_categories"] = categories
        
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                macro_map = macro_data.get('macro_lexicon', macro_data.get('lexicon', {}))
                report["macro_lexicon_status"] = "loaded"
                report["macro_total"] = len(macro_map)
                
                m_categories = {}
                for sym, data in macro_map.items():
                    cat = data.get('category', 'unknown') if isinstance(data, dict) else 'unknown'
                    m_categories[cat] = m_categories.get(cat, 0) + 1
                report["macro_categories"] = m_categories
                
        output_report_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon_audit_report.json')
        with open(output_report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            
        print(f"Audit completed successfully. Report saved to {output_report_path}")
        
    except Exception as e:
        print(f"Error during lexicon audit: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicons()
