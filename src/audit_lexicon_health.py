import sys
import os
import json
import traceback

def audit_lexicon():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    base_dir = os.path.join(workspace, 'TOAI-elegant-lang')
    lexicon_dir = os.path.join(base_dir, 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "timestamp": os.path.getmtime(core_path) if os.path.exists(core_path) else 0,
        "core_lexicon_status": "missing",
        "macro_lexicon_status": "missing",
        "core_categories": {},
        "macro_categories": {},
        "compact_id_stats": {
            "total_symbols": 0,
            "min_id": None,
            "max_id": None,
            "duplicates": []
        }
    }
    
    try:
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            report["core_lexicon_status"] = "loaded"
            
            lexicon_dict = core_data.get("lexicon", {})
            report["compact_id_stats"]["total_symbols"] = len(lexicon_dict)
            
            ids = []
            categories = {}
            for sym, data in lexicon_dict.items():
                if isinstance(data, dict):
                    cat = data.get("category", "unknown")
                    categories[cat] = categories.get(cat, 0) + 1
                    
                    cid = data.get("compact_id")
                    if cid is not None:
                        ids.append(cid)
            
            report["core_categories"] = categories
            if ids:
                report["compact_id_stats"]["min_id"] = min(ids)
                report["compact_id_stats"]["max_id"] = max(ids)
                seen = set()
                dups = set()
                for cid in ids:
                    if cid in seen:
                        dups.add(cid)
                    seen.add(cid)
                report["compact_id_stats"]["duplicates"] = list(dups)
        
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            report["macro_lexicon_status"] = "loaded"
            
            macro_dict = macro_data.get("macros", {})
            m_categories = {}
            for sym, data in macro_dict.items():
                if isinstance(data, dict):
                    cat = data.get("category", "unknown")
                    m_categories[cat] = m_categories.get(cat, 0) + 1
            report["macro_categories"] = m_categories
            
    except Exception as e:
        report["error"] = str(e)
        report["traceback"] = traceback.format_exc()
        
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    audit_lexicon()
