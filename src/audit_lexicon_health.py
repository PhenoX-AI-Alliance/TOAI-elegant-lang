import sys
import os
import json
import traceback

def audit_lexicons():
    base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(base_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "core_lexicon_status": "missing",
        "macro_lexicon_status": "missing",
        "core_stats": {},
        "macro_stats": {}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            report["core_lexicon_status"] = "loaded"
            lex_dict = core_data.get("lexicon", {})
            categories = {}
            compact_ids = []
            for sym, data in lex_dict.items():
                cat = data.get("category", "unknown")
                categories[cat] = categories.get(cat, 0) + 1
                if "compact_id" in data:
                    compact_ids.append(data["compact_id"])
            report["core_stats"] = {
                "total_symbols": len(lex_dict),
                "category_distribution": categories,
                "total_compact_ids": len(compact_ids)
            }
        except Exception as e:
            report["core_lexicon_status"] = f"error: {str(e)}"
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            report["macro_lexicon_status"] = "loaded"
            report["macro_stats"] = {
                "total_macros": len(macro_data) if isinstance(macro_data, dict) else 0
            }
        except Exception as e:
            report["macro_lexicon_status"] = f"error: {str(e)}"
            
    output_path = os.path.join(base_dir, 'TOAI-elegant-lang', 'lexicon_audit_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    audit_lexicons()
