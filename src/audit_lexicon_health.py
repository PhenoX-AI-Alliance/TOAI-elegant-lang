import sys
import os
import json
import traceback

def audit_lexicon():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "core_lexicon": {},
        "macro_lexicon": {},
        "status": "success"
    }
    
    try:
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lexicon_dict = core_data.get('lexicon', {})
                categories = {}
                compact_ids = []
                for sym, data in lexicon_dict.items():
                    cat = data.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    if 'compact_id' in data:
                        compact_ids.append(data['compact_id'])
                report['core_lexicon'] = {
                    "total_entries": len(lexicon_dict),
                    "categories": categories,
                    "compact_id_count": len(compact_ids)
                }
        else:
            report['core_lexicon'] = {"error": "core_lexicon.json not found"}
            
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                report['macro_lexicon'] = {
                    "total_entries": len(macro_data) if isinstance(macro_data, dict) else 0
                }
        else:
            report['macro_lexicon'] = {"error": "macro_lexicon.json not found"}
            
        output_report_path = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon_audit_report.json')
        with open(output_report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print("Audit completed successfully. Report saved to:", output_report_path)
        
    except Exception as e:
        print("Error during lexicon audit:", str(e))
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicon()
