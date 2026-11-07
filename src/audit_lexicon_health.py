import sys
import os
import json
import traceback

def audit_lexicons():
    base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(base_dir, 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "timestamp": os.path.getmtime(core_path) if os.path.exists(core_path) else 0,
        "core_lexicon": {},
        "macro_lexicon": {}
    }
    
    try:
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lex_dict = core_data.get('lexicon', {})
                categories = {}
                compact_ids = []
                for sym, data in lex_dict.items():
                    cat = data.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    cid = data.get('compact_id')
                    if cid is not None:
                        compact_ids.append(cid)
                report['core_lexicon'] = {
                    "total_entries": len(lex_dict),
                    "category_distribution": categories,
                    "compact_id_stats": {
                        "count": len(compact_ids),
                        "min": min(compact_ids) if compact_ids else None,
                        "max": max(compact_ids) if compact_ids else None
                    }
                }
        
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                macro_dict = macro_data.get('macro_lexicon', macro_data)
                if isinstance(macro_dict, dict):
                    m_categories = {}
                    m_compact_ids = []
                    for sym, data in macro_dict.items():
                        if isinstance(data, dict):
                            cat = data.get('category', 'unknown')
                            m_categories[cat] = m_categories.get(cat, 0) + 1
                            cid = data.get('compact_id')
                            if cid is not None:
                                m_compact_ids.append(cid)
                    report['macro_lexicon'] = {
                        "total_entries": len(macro_dict),
                        "category_distribution": m_categories,
                        "compact_id_stats": {
                            "count": len(m_compact_ids),
                            "min": min(m_compact_ids) if m_compact_ids else None,
                            "max": max(m_compact_ids) if m_compact_ids else None
                        }
                    }
    except Exception as e:
        print(f"Error during audit processing: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)
        
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    audit_lexicons()
