import sys
import os
import json
import re
from pathlib import Path

def validate_lexicon(lexicon_path=None):
    if lexicon_path is None:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        lexicon_path = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon', 'core_lexicon.json')
    
    if not os.path.exists(lexicon_path):
        raise FileNotFoundError(f"Required lexicon file not found: {lexicon_path}")
    
    with open(lexicon_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    lex = data.get('lexicon', {})
    if not isinstance(lex, dict):
        raise ValueError("core_lexicon.json must contain a 'lexicon' dictionary.")
    
    required_fields = ['definition', 'japanese', 'category', 'compact_id']
    compact_id_set = set()
    semantic_signatures = {}
    duplicates = []
    
    for sym, item in lex.items():
        if not sym.startswith('§'):
            raise ValueError(f"Symbol '{sym}' must start with '§'")
            
        for field in required_fields:
            if field not in item:
                raise KeyError(f"Symbol '{sym}' is missing required field '{field}'")
                
        # 1. Compact ID 一意性チェック
        cid = item.get('compact_id')
        if cid in compact_id_set:
            raise ValueError(f"Duplicate compact_id detected: {cid} in symbol {sym}")
        compact_id_set.add(cid)
        
        # 2. 意味重複・類似性チェック（語彙インフレ防止）
        # 定義文から重要キーワードを抽出して簡易シグネチャを生成
        clean_def = re.sub(r'[^a-zA-Z0-9\s]', '', item.get('definition', '').lower())
        words = set([w for w in clean_def.split() if len(w) > 4])
        
        # 既存語彙との類似度（Jaccard類似度）
        for prev_sym, prev_words in semantic_signatures.items():
            if not words or not prev_words:
                continue
            intersection = len(words & prev_words)
            union = len(words | prev_words)
            similarity = intersection / union if union > 0 else 0
            if similarity > 0.85: # 類似度85%以上の酷似語彙
                duplicates.append((sym, prev_sym, round(similarity, 2)))
                
        semantic_signatures[sym] = words

    print(f"✅ Lexicon Validation PASSED: {len(lex)} symbols verified.")
    print(f"   - Compact IDs verified: {len(compact_id_set)} unique wire IDs.")
    if duplicates:
        print(f"⚠️ Warning: Found {len(duplicates)} highly overlapping symbols for future consolidation:")
        for s1, s2, sim in duplicates[:5]:
            print(f"     * {s1} <-> {s2} (similarity: {sim})")
    else:
        print("   - Semantic deduplication: No high-risk overlaps detected.")

    return True

if __name__ == '__main__':
    try:
        validate_lexicon()
    except Exception as e:
        print(f"❌ Validation failed: {e}", file=sys.stderr)
        sys.exit(1)
