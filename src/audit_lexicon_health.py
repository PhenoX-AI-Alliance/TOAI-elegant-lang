import sys
import os
import json
import traceback

def audit_lexicons():
    try:
        base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        lexicon_dir = os.path.join(base_dir, 'TOAI-elegant-lang', 'lexicon')
        
        core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
        macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
        
        report = {
            "core_lexicon_exists": os.path.exists(core_path),
            "macro_lexicon_exists": os.path.exists(macro_path),
            "core_stats": {},
            "macro_stats": {}
        }
        
        if report["core_lexicon_exists"]:
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
                        
            report["core_stats"] = {
                "total_entries": len(lexicon_dict),
                "category_distribution": categories,
                "total_compact_ids": len(compact_ids)
            }
            
        if report["macro_lexicon_exists"]:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            report["macro_stats"] = {
                "total_entries": len(macro_data) if isinstance(macro_data, dict) else 0
            }
            
        print(json.dumps(report, ensure_ascii=False, indent=2))
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicons()
