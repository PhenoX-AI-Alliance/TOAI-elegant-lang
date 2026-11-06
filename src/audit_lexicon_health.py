import sys
import os
import traceback
import json

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "core_lexicon": {"status": "missing", "total_symbols": 0, "categories": {}, "compact_id_stats": {}},
        "macro_lexicon": {"status": "missing", "total_macros": 0, "categories": {}}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            
            lexicon_dict = core_data.get('lexicon', {})
            total_syms = len(lexicon_dict)
            categories = {}
            compact_ids = []
            
            for sym, data in lexicon_dict.items():
                cat = data.get('category', 'unknown')
                categories[cat] = categories.get(cat, 0) + 1
                if 'compact_id' in data:
                    compact_ids.append(data['compact_id'])
            
            report["core_lexicon"] = {
                "status": "loaded",
                "total_symbols": total_syms,
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
            
            macros = macro_data.get('macros', {})
            total_macros = len(macros)
            m_categories = {}
            
            for m_name, m_val in macros.items():
                cat = m_val.get('category', 'unknown')
                m_categories[cat] = m_categories.get(cat, 0) + 1
                
            report["macro_lexicon"] = {
                "status": "loaded",
                "total_macros": total_macros,
                "categories": m_categories
            }
        except Exception as e:
            report["macro_lexicon"]["status"] = f"error: {str(e)}"
            
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        audit_lexicons()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)