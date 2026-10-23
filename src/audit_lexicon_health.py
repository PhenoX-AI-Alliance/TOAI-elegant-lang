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
        "core_lexicon": {"status": "missing", "total_symbols": 0, "categories": {}, "compact_id_stats": {}},
        "macro_lexicon": {"status": "missing", "total_entries": 0, "categories": {}}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            lexicon = core_data.get('lexicon', {})
            categories = {}
            compact_ids = []
            
            for sym, data in lexicon.items():
                cat = data.get('category', 'unknown')
                categories[cat] = categories.get(cat, 0) + 1
                
                if 'compact_id' in data:
                    compact_ids.append(data['compact_id'])
            
            report["core_lexicon"] = {
                "status": "loaded",
                "total_symbols": len(lexicon),
                "categories": categories,
                "compact_id_stats": {
                    "count": len(compact_ids),
                    "min": min(compact_ids) if compact_ids else None,
                    "max": max(compact_ids) if compact_ids else None
                }
            }
        except Exception as e:
            report["core_lexicon"]["status"] = f"error: {str(e)}"
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            
            macro_entries = macro_data.get('macros', macro_data) if isinstance(macro_data, dict) else macro_data
            if isinstance(macro_entries, dict):
                total_macro = len(macro_entries)
                macro_cats = {}
                for m_key, m_val in macro_entries.items():
                    if isinstance(m_val, dict):
                        m_cat = m_val.get('category', 'unknown')
                        macro_cats[m_cat] = macro_cats.get(m_cat, 0) + 1
            else:
                total_macro = len(macro_entries)
                macro_cats = {"default": total_macro}
                
            report["macro_lexicon"] = {
                "status": "loaded",
                "total_entries": total_macro,
                "categories": macro_cats
            }
        except Exception as e:
            report["macro_lexicon"]["status"] = f"error: {str(e)}"
            
    output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'lexicon_audit_report.json')
    with open(output_path, 'w', encoding='utf-8') as out_f:
        json.dump(report, out_f, indent=2, ensure_ascii=False)
        
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    try:
        audit_lexicons()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)