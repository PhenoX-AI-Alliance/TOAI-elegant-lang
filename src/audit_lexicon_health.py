import sys
import os
import traceback
import time
import json

def audit_lexicon():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "timestamp": time.time(),
        "core_lexicon": {},
        "macro_lexicon": {}
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
                    "total_symbols": len(lexicon_dict),
                    "category_distribution": categories,
                    "compact_id_count": len(compact_ids)
                }
        except Exception as e:
            report['core_lexicon']['error'] = str(e)
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                report['macro_lexicon'] = {
                    "total_macros": len(macro_data) if isinstance(macro_data, dict) else 0
                }
        except Exception as e:
            report['macro_lexicon']['error'] = str(e)
            
    output_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon_health_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    try:
        audit_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
