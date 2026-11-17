import sys
import os
import json
import traceback

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    base_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    core_path = os.path.join(base_dir, 'lexicon', 'core_lexicon.json')
    macro_path = os.path.join(base_dir, 'lexicon', 'macro_lexicon.json')
    
    result = {
        "core_lexicon": {},
        "macro_lexicon": {}
    }
    
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
            result["core_lexicon"] = {
                "total_entries": len(lexicon_dict),
                "categories": categories,
                "compact_id_count": len(compact_ids)
            }
            
    if os.path.exists(macro_path):
        with open(macro_path, 'r', encoding='utf-8') as f:
            macro_data = json.load(f)
            if isinstance(macro_data, dict):
                m_categories = {}
                for k, v in macro_data.items():
                    if isinstance(v, dict):
                        cat = v.get('category', 'unknown')
                        m_categories[cat] = m_categories.get(cat, 0) + 1
                result["macro_lexicon"] = {
                    "total_entries": len(macro_data),
                    "categories": m_categories
                }
                
    output_path = os.path.join(base_dir, 'lexicon', 'audit_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        audit_lexicons()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
