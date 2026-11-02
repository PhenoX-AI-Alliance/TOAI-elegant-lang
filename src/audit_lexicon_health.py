import sys
import os
import json
import traceback

def audit_lexicon():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    results = {
        "core_lexicon": {},
        "macro_lexicon": {},
        "timestamp": os.path.exists(core_path)
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lex_dict = core_data.get('lexicon', {})
                categories = {}
                compact_ids = []
                for sym, data in lex_dict.items():
                    cat = data.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    if 'compact_id' in data:
                        compact_ids.append(data['compact_id'])
                results["core_lexicon"] = {
                    "total_entries": len(lex_dict),
                    "categories": categories,
                    "compact_id_stats": {
                        "min": min(compact_ids) if compact_ids else None,
                        "max": max(compact_ids) if compact_ids else None,
                        "count": len(compact_ids)
                    }
                }
        except Exception as e:
            results["core_lexicon"]["error"] = str(e)
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                lex_dict = macro_data.get('lexicon', {})
                categories = {}
                compact_ids = []
                for sym, data in lex_dict.items():
                    cat = data.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    if 'compact_id' in data:
                        compact_ids.append(data['compact_id'])
                results["macro_lexicon"] = {
                    "total_entries": len(lex_dict),
                    "categories": categories,
                    "compact_id_stats": {
                        "min": min(compact_ids) if compact_ids else None,
                        "max": max(compact_ids) if compact_ids else None,
                        "count": len(compact_ids)
                    }
                }
        except Exception as e:
            results["macro_lexicon"]["error"] = str(e)
            
    output_path = os.path.join(lexicon_dir, 'lexicon_audit_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    audit_lexicon()
