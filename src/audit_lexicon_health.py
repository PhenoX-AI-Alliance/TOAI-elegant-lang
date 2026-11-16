import sys
import os
import traceback
import json

def audit():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    
    # Check multiple possible locations for lexicon files to prevent FileNotFoundError
    possible_base_dirs = [
        os.path.join(workspace_dir, 'TOAI-elegant-lang'),
        workspace_dir
    ]
    
    core_path = None
    macro_path = None
    
    for base in possible_base_dirs:
        c_p = os.path.join(base, 'lexicon', 'core_lexicon.json')
        m_p = os.path.join(base, 'lexicon', 'macro_lexicon.json')
        if os.path.exists(c_p) and core_path is None:
            core_path = c_p
        if os.path.exists(m_p) and macro_path is None:
            macro_path = m_p
            
    # Fallback paths if not found
    if not core_path:
        core_path = os.path.join(workspace_dir, 'lexicon', 'core_lexicon.json')
    if not macro_path:
        macro_path = os.path.join(workspace_dir, 'lexicon', 'macro_lexicon.json')
        
    print(f"Target core_path: {core_path}")
    print(f"Target macro_path: {macro_path}")
    
    core_data = {}
    macro_data = {}
    
    if os.path.exists(core_path):
        with open(core_path, 'r', encoding='utf-8') as f:
            core_data = json.load(f)
    else:
        print(f"Warning: {core_path} does not exist. Using empty dict.")
        
    if os.path.exists(macro_path):
        with open(macro_path, 'r', encoding='utf-8') as f:
            macro_data = json.load(f)
    else:
        print(f"Warning: {macro_path} does not exist. Using empty dict.")
        
    lexicon_dict = core_data.get('lexicon', core_data)
    
    categories = {}
    compact_ids = []
    
    for sym, data in lexicon_dict.items():
        if isinstance(data, dict):
            cat = data.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
            cid = data.get('compact_id')
            if cid is not None:
                compact_ids.append(cid)
                
    audit_result = {
        "total_entries": len(lexicon_dict),
        "categories": categories,
        "compact_id_count": len(compact_ids),
        "macro_entries_count": len(macro_data) if isinstance(macro_data, dict) else 0
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'lexicon_audit_report.json')
    
    with open(output_path, 'w', encoding='utf-8') as out_f:
        json.dump(audit_result, out_f, indent=2, ensure_ascii=False)
        
    print(json.dumps(audit_result, indent=2, ensure_ascii=False))
    print(f"Audit report successfully saved to {output_path}")

if __name__ == '__main__':
    try:
        audit()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
