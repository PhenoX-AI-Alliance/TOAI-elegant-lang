import sys
import os
import traceback
import json

def load_json_safe(filepath):
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
        return None

def audit_lexicon():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    core_data = load_json_safe(core_path)
    macro_data = load_json_safe(macro_path)
    
    audit_results = {
        "core_lexicon_status": "missing",
        "macro_lexicon_status": "missing",
        "core_categories": {},
        "macro_categories": {},
        "core_compact_ids": [],
        "macro_compact_ids": [],
        "errors": []
    }
    
    if core_data is not None:
        audit_results["core_lexicon_status"] = "loaded"
        lexicon_dict = core_data.get('lexicon', {})
        if isinstance(lexicon_dict, dict):
            categories = {}
            compact_ids = []
            for sym, data in lexicon_dict.items():
                if isinstance(data, dict):
                    cat = data.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    if 'compact_id' in data:
                        compact_ids.append(data.get('compact_id'))
            audit_results["core_categories"] = categories
            audit_results["core_compact_ids_count"] = len(compact_ids)
        else:
            audit_results["errors"]["core"] = "Invalid lexicon format: 'lexicon' is not a dict."
    else:
        audit_results["errors"].append(f"Could not load {core_path}")
        
    if macro_data is not None:
        audit_results["macro_lexicon_status"] = "loaded"
        macro_dict = macro_data.get('macro_lexicon', macro_data.get('lexicon', {}))
        if isinstance(macro_dict, dict):
            categories = {}
            compact_ids = []
            for sym, data in macro_dict.items():
                if isinstance(data, dict):
                    cat = data.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    if 'compact_id' in data:
                        compact_ids.append(data.get('compact_id'))
            audit_results["macro_categories"] = categories
            audit_results["macro_compact_ids_count"] = len(compact_ids)
        else:
            audit_results["errors"]["macro"] = "Invalid macro lexicon format."
    else:
        audit_results["errors"].append(f"Could not load {macro_path}")
        
    output_audit_path = os.path.join(workspace_dir, 'TOAI_Generated', 'lexicon_audit_report.json')
    os.makedirs(os.path.dirname(output_audit_path), exist_ok=True)
    
    try:
        with open(output_audit_path, 'w', encoding='utf-8') as f:
            json.dump(audit_results, f, ensure_ascii=False, indent=2)
        print(f"Audit report successfully written to {output_audit_path}")
    except Exception as e:
        print(f"Failed to write audit report: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    try:
        audit_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
