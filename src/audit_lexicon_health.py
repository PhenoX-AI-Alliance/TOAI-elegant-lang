import sys
import os
import json
import traceback

def audit_lexicon():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "core_lexicon": {"status": "missing", "total_symbols": 0, "categories": {}, "compact_id_stats": {}},
        "macro_lexicon": {"status": "missing", "total_symbols": 0, "categories": {}, "compact_id_stats": {}}
    }
    
    try:
        if os.path.exists(core_path):
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
        
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            lexicon = macro_data.get('lexicon', macro_data) if isinstance(macro_data, dict) else {}
            if isinstance(lexicon, dict):
                categories = {}
                compact_ids = []
                for sym, data in lexicon.items():
                    if isinstance(data, dict):
                        cat = data.get('category', 'unknown')
                        categories[cat] = categories.get(cat, 0) + 1
                        if 'compact_id' in data:
                            compact_ids.append(data['compact_id'])
                report["macro_lexicon"] = {
                    "status": "loaded",
                    "total_symbols": len(lexicon),
                    "categories": categories,
                    "compact_id_stats": {
                        "count": len(compact_ids),
                        "min": min(compact_ids) if compact_ids else None,
                        "max": max(compact_ids) if compact_ids else None
                    }
                }
        
        output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'lexicon_audit_report.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"Audit report successfully generated at: {output_path}")
        
    except Exception as e:
        print(f"Error during lexicon audit: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicon()
