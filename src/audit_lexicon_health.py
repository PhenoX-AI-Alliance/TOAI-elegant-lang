import sys
import os
import json
import traceback

def audit_lexicons():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    base_dir = os.path.join(workspace, 'TOAI-elegant-lang')
    lexicon_dir = os.path.join(base_dir, 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "timestamp": os.path.getmtime(core_path) if os.path.exists(core_path) else 0,
        "core_lexicon": {"total_symbols": 0, "categories": {}, "compact_id_stats": {}},
        "macro_lexicon": {"total_macros": 0, "categories": {}}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lexicon_dict = core_data.get('lexicon', {})
                report["core_lexicon"]["total_symbols"] = len(lexicon_dict)
                
                categories = {}
                compact_ids = []
                for sym, data in lexicon_dict.items():
                    cat = data.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    
                    cid = data.get('compact_id')
                    if cid is not None:
                        compact_ids.append(cid)
                
                report["core_lexicon"]["categories"] = categories
                if compact_ids:
                    report["core_lexicon"]["compact_id_stats"] = {
                        "min": min(compact_ids),
                        "max": max(compact_ids),
                        "count": len(compact_ids)
                    }
        except Exception as e:
            report["core_lexicon"]["error"] = str(e)
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                if isinstance(macro_data, dict):
                    macros = macro_data.get('macros', macro_data)
                    report["macro_lexicon"]["total_macros"] = len(macros)
                    macro_cats = {}
                    for m_name, m_val in macros.items():
                        if isinstance(m_val, dict):
                            m_cat = m_val.get('category', 'unknown')
                            macro_cats[m_cat] = macro_cats.get(m_cat, 0) + 1
                    report["macro_lexicon"]["categories"] = macro_cats
        except Exception as e:
            report["macro_lexicon"]["error"] = str(e)
            
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report

if __name__ == '__main__':
    audit_lexicons()
