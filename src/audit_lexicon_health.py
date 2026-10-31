import sys
import os
import traceback
import json

def load_json(filepath):
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {{filepath}}: {{e}}", file=sys.stderr)
        return {}

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    core_data = load_json(core_path)
    macro_data = load_json(macro_path)
    
    lexicon_dict = core_data.get('lexicon', {})
    
    category_counts = {}
    compact_id_stats = {
        'total_items': len(lexicon_dict),
        'missing_compact_id': 0,
        'unique_compact_ids': set()
    }
    
    for sym, data in lexicon_dict.items():
        if isinstance(data, dict):
            cat = data.get('category', 'uncategorized')
            category_counts[cat] = category_counts.get(cat, 0) + 1
            
            cid = data.get('compact_id')
            if cid is not None:
                compact_id_stats['unique_compact_ids'].add(cid)
            else:
                compact_id_stats['missing_compact_id'] += 1
        else:
            category_counts['malformed'] = category_counts.get('malformed', 0) + 1
            compact_id_stats['missing_compact_id'] += 1

    compact_id_stats['unique_compact_ids'] = len(compact_id_stats['unique_compact_ids'])
    
    audit_report = {
        'status': 'success',
        'core_lexicon_path': core_path,
        'macro_lexicon_path': macro_path,
        'category_distribution': category_counts,
        'compact_id_statistics': compact_id_stats,
        'macro_lexicon_keys': list(macro_data.keys()) if isinstance(macro_data, dict) else []
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'lexicon_audit_report.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(audit_report, f, ensure_ascii=False, indent=2)
        
    print(json.dumps(audit_report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        audit_lexicons()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
