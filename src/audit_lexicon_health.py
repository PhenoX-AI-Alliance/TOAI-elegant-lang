import sys
import os
import json
import traceback

def audit_lexicons():
    base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    elegant_dir = os.path.join(base_dir, 'TOAI-elegant-lang')
    
    core_path = os.path.join(elegant_dir, 'lexicon', 'core_lexicon.json')
    macro_path = os.path.join(elegant_dir, 'lexicon', 'macro_lexicon.json')
    
    report = {
        "core_lexicon_status": "missing",
        "macro_lexicon_status": "missing",
        "core_categories": {},
        "macro_categories": {},
        "core_count": 0,
        "macro_count": 0,
        "compact_id_stats": {}
    }
    
    try:
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                report["core_lexicon_status"] = "loaded"
                lexicon_map = core_data.get('lexicon', {})
                report["core_count"] = len(lexicon_map)
                
                categories = {}
                compact_lengths = []
                for sym, data in lexicon_map.items():
                    cat = data.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    
                    cid = data.get('compact_id')
                    if cid is not None:
                        compact_lengths.append(len(str(cid)))
                        
                report["core_categories"] = categories
                if compact_lengths:
                    report["compact_id_stats"]["min_length"] = min(compact_lengths)
                    report["compact_id_stats"]["max_length"] = max(compact_lengths)
                    report["compact_id_stats"]["avg_length"] = sum(compact_lengths) / len(compact_lengths)
        
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                report["macro_lexicon_status"] = "loaded"
                macro_map = macro_data.get('macro_lexicon', macro_data)
                if isinstance(macro_map, dict):
                    report["macro_count"] = len(macro_map)
                    macro_cats = {}
                    for sym, data in macro_map.items():
                        if isinstance(data, dict):
                            cat = data.get('category', 'unknown')
                            macro_cats[cat] = macro_cats.get(cat, 0) + 1
                    report["macro_categories"] = macro_cats
                    
        output_dir = os.path.join(elegant_dir, 'reports')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'lexicon_audit_report.json')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            
        print(f"Audit completed successfully. Report saved to {output_path}")
        
    except Exception as e:
        print(f"Error during lexicon audit: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicons()
