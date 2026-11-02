import sys
import os
import json
import traceback

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    audit_results = {
        'timestamp': os.path.exists(core_path) and os.path.getmtime(core_path) or 0,
        'core_lexicon': {},
        'macro_lexicon': {}
    }
    
    if os.path.exists(core_path):
        try:
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
                audit_results['core_lexicon'] = {
                    'total_symbols': len(lexicon),
                    'category_distribution': categories,
                    'compact_id_count': len(compact_ids)
                }
        except Exception as e:
            audit_results['core_lexicon']['error'] = str(e)
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                lexicon = macro_data.get('lexicon', {})
                categories = {}
                for sym, data in lexicon.items():
                    cat = data.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                audit_results['macro_lexicon'] = {
                    'total_symbols': len(lexicon),
                    'category_distribution': categories
                }
        except Exception as e:
            audit_results['macro_lexicon']['error'] = str(e)
            
    output_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon', 'audit_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(audit_results, f, ensure_ascii=False, indent=2)
    print(json.dumps(audit_results, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        audit_lexicons()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
