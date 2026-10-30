import sys
import os
import json
import time

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    core_lexicon_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_lexicon_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    if not os.path.exists(core_lexicon_path):
        print(f"Error: {core_lexicon_path} not found.", file=sys.stderr)
        sys.exit(1)
        
    with open(core_lexicon_path, 'r', encoding='utf-8') as f:
        core_data = json.load(f)
        
    macro_data = {}
    if os.path.exists(macro_lexicon_path):
        with open(macro_lexicon_path, 'r', encoding='utf-8') as f:
            macro_data = json.load(f)
            
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
                
    report = {
        'timestamp': time.time(),
        'total_entries': len(lexicon_dict),
        'category_distribution': categories,
        'compact_id_stats': {
            'count': len(compact_ids),
            'min': min(compact_ids) if compact_ids else None,
            'max': max(compact_ids) if compact_ids else None
        },
        'macro_entries_count': len(macro_data.get('macro_lexicon', {}))
    }
    
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    audit_lexicons()
