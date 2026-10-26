import sys
import os
import json

def audit():
    base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(base_dir, 'lexicon')
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    def load(p):
        if not os.path.exists(p):
            return {}
        with open(p, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    core = load(core_path)
    macro = load(macro_path)
    
    def process(data):
        lex = data.get('lexicon', {})
        cat_dist = {}
        cids = []
        for k, v in lex.items():
            if isinstance(v, dict):
                c = v.get('category', 'unknown')
                cat_dist[c] = cat_dist.get(c, 0) + 1
                cid = v.get('compact_id')
                if cid is not None:
                    cids.append(cid)
        return {
            "total": len(lex),
            "categories": cat_dist,
            "compact_id_min": min(cids) if cids else None,
            "compact_id_max": max(cids) if cids else None
        }
        
    result = {
        "core": process(core),
        "macro": process(macro)
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    audit()
