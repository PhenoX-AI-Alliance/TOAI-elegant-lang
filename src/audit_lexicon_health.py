import sys
import os
import traceback
import time
import json

def load_json(filepath):
    if not os.path.exists(filepath):
        return {}
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def audit_lexicon():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    core_data = load_json(core_path)
    macro_data = load_json(macro_path)
    
    lexicon_dict = core_data.get('lexicon', {})
    
    category_counts = {}
    compact_ids = []
    
    for sym, data in lexicon_dict.items():
        if isinstance(data, dict):
            cat = data.get('category', 'unknown')
            category_counts[cat] = category_counts.get(cat, 0) + 1
            
            cid = data.get('compact_id')
            if cid is not None:
                compact_ids.append(cid)
                
    audit_result = {
        'timestamp': time.time(),
        'total_entries': len(lexicon_dict),
        'category_distribution': category_counts,
        'compact_id_stats': {
            'count': len(compact_ids),
            'min': min(compact_ids) if compact_ids else None,
            'max': max(compact_ids) if compact_ids else None
        },
        'macro_lexicon_keys': list(macro_data.keys()) if isinstance(macro_data, dict) else []
    }
    
    out_dir = os.path.join(workspace, 'TOAI-elegant-lang', 'audit_reports')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'lexicon_health_report.json')
    
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(audit_result, f, indent=2, ensure_ascii=False)
        
    print(json.dumps(audit_result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    try:
        audit_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
