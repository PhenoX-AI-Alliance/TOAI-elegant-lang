import sys
import os
import json

def audit_lexicons():
    base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    elegant_dir = os.path.join(base_dir, 'TOAI-elegant-lang')
    
    core_path = os.path.join(elegant_dir, 'lexicon', 'core_lexicon.json')
    macro_path = os.path.join(elegant_dir, 'lexicon', 'macro_lexicon.json')
    
    audit_result = {
        "timestamp": os.path.exists(core_path) and os.path.getmtime(core_path) or 0,
        "core_lexicon": {},
        "macro_lexicon": {}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lexicon = core_data.get('lexicon', {})
                categories = {}
                compact_ids = []
                for sym, data in lexicon.items():
                    if isinstance(data, dict):
                        cat = data.get('category', 'unknown')
                        categories[cat] = categories.get(cat, 0) + 1
                        if 'compact_id' in data:
                            compact_ids.append(data['compact_id'])
                audit_result["core_lexicon"] = {
                    "total_symbols": len(lexicon),
                    "categories": categories,
                    "compact_id_count": len(compact_ids)
                }
        except Exception as e:
            audit_result["core_lexicon"] = {"error": str(e)}
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                audit_result["macro_lexicon"] = {
                    "total_macros": len(macro_data) if isinstance(macro_data, dict) else 0
                }
        except Exception as e:
            audit_result["macro_lexicon"] = {"error": str(e)}
            
    print(json.dumps(audit_result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    audit_lexicons()
