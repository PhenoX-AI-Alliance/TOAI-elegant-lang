import sys
import os
import json
import traceback

def audit_lexicons():
    base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    elegant_dir = os.path.join(base_dir, 'TOAI-elegant-lang')
    lexicon_dir = os.path.join(elegant_dir, 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    results = {
        "core_lexicon": {"status": "missing", "category_distribution": {}, "compact_id_stats": {}},
        "macro_lexicon": {"status": "missing", "category_distribution": {}, "compact_id_stats": {}}
    }
    
    if os.path.exists(core_path):
        try:
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
            
            results["core_lexicon"]["status"] = "success"
            results["core_lexicon"]["category_distribution"] = categories
            results["core_lexicon"]["compact_id_stats"] = {
                "total_items": len(lexicon_dict),
                "has_compact_id_count": len(compact_ids),
                "min": min(compact_ids) if compact_ids else None,
                "max": max(compact_ids) if compact_ids else None
            }
        except Exception as e:
            results["core_lexicon"]["status"] = f"error: {str(e)}"
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            
            macro_dict = macro_data.get('lexicon', macro_data)
            if isinstance(macro_dict, dict):
                categories = {}
                compact_ids = []
                for sym, data in macro_dict.items():
                    if isinstance(data, dict):
                        cat = data.get('category', 'unknown')
                        categories[cat] = categories.get(cat, 0) + 1
                        if 'compact_id' in data:
                            compact_ids.append(data['compact_id'])
                
                results["macro_lexicon"]["status"] = "success"
                results["macro_lexicon"]["category_distribution"] = categories
                results["macro_lexicon"]["compact_id_stats"] = {
                    "total_items": len(macro_dict),
                    "has_compact_id_count": len(compact_ids)
                }
            else:
                results["macro_lexicon"]["status"] = "error: invalid format"
        except Exception as e:
            results["macro_lexicon"]["status"] = f"error: {str(e)}"
            
    output_path = os.path.join(base_dir, 'TOAI_Generated', 'lexicon_audit_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        audit_lexicons()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
