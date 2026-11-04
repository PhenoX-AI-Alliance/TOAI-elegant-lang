import sys
import os
import json
import traceback

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    audit_report = {
        "timestamp": os.path.getmtime(core_path) if os.path.exists(core_path) else 0,
        "core_lexicon_stats": {},
        "macro_lexicon_stats": {}
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
                    
            audit_report['core_lexicon_stats'] = {
                "total_entries": len(lexicon_dict),
                "categories": categories,
                "compact_id_count": len(compact_ids),
                "has_duplicates": len(compact_ids) != len(set(compact_ids))
            }
        else:
            audit_report['core_lexicon_stats'] = {"error": "core_lexicon.json not found"}
            
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            audit_report['macro_lexicon_stats'] = {
                "total_entries": len(macro_data) if isinstance(macro_data, dict) else 0
            }
        else:
            audit_report['macro_lexicon_stats'] = {"error": "macro_lexicon.json not found"}
            
        report_path = os.path.join(workspace_dir, 'TOAI_Generated', 'lexicon_audit_report.json')
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(audit_report, f, ensure_ascii=False, indent=2)
            
        print(json.dumps(audit_report, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"Error during audit: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicons()
