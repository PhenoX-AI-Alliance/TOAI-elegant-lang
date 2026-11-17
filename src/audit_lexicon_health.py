import sys
import os
import json
import traceback

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    elegant_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    core_path = os.path.join(elegant_dir, 'lexicon', 'core_lexicon.json')
    macro_path = os.path.join(elegant_dir, 'lexicon', 'macro_lexicon.json')
    output_path = os.path.join(elegant_dir, 'lexicon', 'audit_report.json')
    
    report = {
        'timestamp': os.popen('date -u +%Y-%m-%dT%H:%M:%SZ').read().strip(),
        'core_lexicon': {},
        'macro_lexicon': {}
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
            
            report['core_lexicon'] = {
                'total_symbols': len(lexicon_dict),
                'categories': categories,
                'compact_id_count': len(compact_ids),
                'min_compact_id': min(compact_ids) if compact_ids else None,
                'max_compact_id': max(compact_ids) if compact_ids else None
            }
        except Exception as e:
            report['core_lexicon']['error'] = str(e)
    else:
        report['core_lexicon']['error'] = 'core_lexicon.json not found'
        
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            report['macro_lexicon'] = {
                'total_macros': len(macro_data),
                'keys': list(macro_data.keys())
            }
        except Exception as e:
            report['macro_lexicon']['error'] = str(e)
    else:
        report['macro_lexicon']['error'] = 'macro_lexicon.json not found'
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    try:
        audit_lexicons()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
