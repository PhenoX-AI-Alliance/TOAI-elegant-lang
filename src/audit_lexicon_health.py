import sys
import os
import traceback
import json

def load_json_file(file_path):
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    core_data = load_json_file(core_path)
    macro_data = load_json_file(macro_path)
    
    audit_results = {
        "timestamp": os.path.getmtime(core_path) if os.path.exists(core_path) else 0,
        "core_lexicon_status": "missing",
        "macro_lexicon_status": "missing",
        "core_stats": {},
        "macro_stats": {}
    }
    
    if core_data and isinstance(core_data, dict):
        audit_results["core_lexicon_status"] = "loaded"
        lexicon_dict = core_data.get('lexicon', {})
        categories = {}
        compact_ids = []
        
        for sym, data in lexicon_dict.items():
            if isinstance(data, dict):
                cat = data.get('category', 'unknown')
                categories[cat] = categories.get(cat, 0) + 1
                
                cid = data.get('compact_id')
                if cid is not None:
                    compact_ids.append(cid)
                    
        audit_results["core_stats"] = {
            "total_symbols": len(lexicon_dict),
            "category_distribution": categories,
            "compact_id_count": len(compact_ids),
            "compact_id_min": min(compact_ids) if compact_ids else None,
            "compact_id_max": max(compact_ids) if compact_ids else None
        }
        
    if macro_data and isinstance(macro_data, dict):
        audit_results["macro_lexicon_status"] = "loaded"
        audit_results["macro_stats"] = {
            "total_keys": len(macro_data)
        }
        
    output_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'audit_reports')
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, 'lexicon_health_report.json')
    
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(audit_results, f, ensure_ascii=False, indent=2)
        print(f"Successfully audited lexicons. Report saved to {report_path}")
    except Exception as e:
        print(f"Failed to save audit report: {e}")
        sys.exit(1)

if __name__ == '__main__':
    try:
        audit_lexicons()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)