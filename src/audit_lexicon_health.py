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
        "timestamp": os.path.exists(core_path) and os.path.getmtime(core_path) or 0,
        "core_lexicon": {},
        "macro_lexicon": {}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lexicon_dict = core_data.get('lexicon', {})
                categories = {}
                compact_ids = []
                for sym, data in lexicon_dict.items():
                    if isinstance(data, dict):
                        cat = data.get('category', 'unknown')
                        categories[cat] = categories.get(cat, 0) + 1
                        if 'compact_id' in data:
                            compact_ids.append(data['compact_id'])
                report['core_lexicon'] = {
                    "total_entries": len(lexicon_dict),
                    "categories": categories,
                    "compact_id_count": len(compact_ids)
                }
        except Exception as e:
            report['core_lexicon'] = {"error": str(e)}
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                report['macro_lexicon'] = {
                    "total_entries": len(macro_data) if isinstance(macro_data, (dict, list)) else 0
                }
        except Exception as e:
            report['macro_lexicon'] = {"error": str(e)}
            
    output_path = os.path.join(base_dir, 'TOAI-elegant-lang', 'lexicon_audit_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"Audit report successfully written to {output_path}")

if __name__ == '__main__':
    audit_lexicons()
