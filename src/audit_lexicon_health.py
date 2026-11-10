import os
import json
import sys

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        'core_lexicon': {},
        'macro_lexicon': {},
        'timestamp': os.path.getmtime(core_path) if os.path.exists(core_path) else 0
    }
    
    if os.path.exists(core_path):
        with open(core_path, 'r', encoding='utf-8') as f:
            core_data = json.load(f)
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
            report['core_lexicon'] = {
                'total_symbols': len(lexicon_dict),
                'category_distribution': categories,
                'compact_id_count': len(compact_ids),
                'compact_id_min': min(compact_ids) if compact_ids else None,
                'compact_id_max': max(compact_ids) if compact_ids else None
            }
            
    if os.path.exists(macro_path):
        with open(macro_path, 'r', encoding='utf-8') as f:
            macro_data = json.load(f)
            if isinstance(macro_data, dict):
                macro_list = macro_data.get('macros', macro_data)
                report['macro_lexicon'] = {
                    'total_macros': len(macro_list)
                }
            else:
                report['macro_lexicon'] = {
                    'total_macros': len(macro_data)
                }
                
    output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'lexicon_audit_report.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    audit_lexicons()
