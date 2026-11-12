import sys
import os
import json
import traceback

def audit_lexicons():
    try:
        base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        lang_dir = os.path.join(base_dir, 'TOAI-elegant-lang')
        
        core_path = os.path.join(lang_dir, 'lexicon', 'core_lexicon.json')
        macro_path = os.path.join(lang_dir, 'lexicon', 'macro_lexicon.json')
        
        report = {
            "timestamp": os.path.getmtime(core_path) if os.path.exists(core_path) else 0,
            "core_lexicon": {"exists": False, "total_symbols": 0, "categories": {}, "compact_id_stats": {}},
            "macro_lexicon": {"exists": False, "total_symbols": 0, "categories": {}, "compact_id_stats": {}}
        }
        
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            lexicon = core_data.get('lexicon', {})
            report["core_lexicon"]["exists"] = True
            report["core_lexicon"]["total_symbols"] = len(lexicon)
            
            categories = {}
            compact_ids = []
            for sym, data in lexicon.items():
                cat = data.get('category', 'unknown')
                categories[cat] = categories.get(cat, 0) + 1
                if 'compact_id' in data:
                    compact_ids.append(data['compact_id'])
            
            report["core_lexicon"]["categories"] = categories
            report["core_lexicon"]["compact_id_stats"] = {
                "count": len(compact_ids),
                "min": min(compact_ids) if compact_ids else None,
                "max": max(compact_ids) if compact_ids else None
            }
            
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            lexicon = macro_data.get('lexicon', {}) if isinstance(macro_data, dict) and 'lexicon' in macro_data else macro_data
            if isinstance(lexicon, dict):
                report["macro_lexicon"]["exists"] = True
                report["macro_lexicon"]["total_symbols"] = len(lexicon)
                categories = {}
                for sym, data in lexicon.items():
                    if isinstance(data, dict):
                        cat = data.get('category', 'unknown')
                        categories[cat] = categories.get(cat, 0) + 1
                report["macro_lexicon"]["categories"] = categories
                
        output_path = os.path.join(lang_dir, 'lexicon', 'audit_report.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            
        print(json.dumps(report, ensure_ascii=False, indent=2))
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicons()
