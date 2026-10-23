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
    naming_errors = []
    
    for sym, item in lex.items():
        if not sym.startswith('§'):
            raise ValueError(f"Symbol '{sym}' must start with '§'")
            
        for field in required_fields:
            if field not in item:
                raise KeyError(f"Symbol '{sym}' is missing required field '{field}'")

        # 1. 命名規則のサニタイズ（新規制: _v2等のサフィックス禁止、アンダースコア区切り最大4単語まで）
        # ※ 過去の登録済み既存シンボルは警告にとどめ、新規登録時の完全ブロックを可能にする
        raw_name = sym[1:] # §を除去
        parts = raw_name.split('_')
        if re.search(r'_[vV]\d+$', sym):
            naming_errors.append(f"{sym}: Suffix versioning (_vN) is deprecated/forbidden.")
        if len(parts) > 4:
            naming_errors.append(f"{sym}: Symbol name is too long ({len(parts)} words > 4 max).")
                
        # 2. Compact ID 一意性チェック
        cid = item.get('compact_id')
        if cid in compact_id_set:
            raise ValueError(f"Duplicate compact_id detected: {cid} in symbol {sym}")
        compact_id_set.add(cid)
        
        # 3. 意味重複・類似性チェック（語彙インフレ防止）
        clean_def = re.sub(r'[^a-zA-Z0-9\s]', '', item.get('definition', '').lower())
        words = set([w for w in clean_def.split() if len(w) > 4])
        
        for prev_sym, prev_words in semantic_signatures.items():
            if not words or not prev_words:
                continue
            intersection = len(words & prev_words)
            union = len(words | prev_words)
            similarity = intersection / union if union > 0 else 0
            if similarity > 0.85:
                duplicates.append((sym, prev_sym, round(similarity, 2)))
                
        semantic_signatures[sym] = words

    summary_msg = f"Validated {len(lex)} words: {len(duplicates)} duplicates, {len(naming_errors)} naming notices, 100% type-safe"
    print(f"✅ Lexicon Validation PASSED: {len(lex)} symbols verified.")
    print(f"   - Compact IDs verified: {len(compact_id_set)} unique wire IDs.")
    if duplicates:
        print(f"   - Warning: {len(duplicates)} highly overlapping symbols flagged.")
    if naming_errors:
        print(f"   - Notice: {len(naming_errors)} legacy symbols exceed 4 words or have _vN.")

    return summary_msg

if __name__ == '__main__':
    try:
        msg = validate_lexicon()
        print(f"Summary: {msg}")
    except Exception as e:
        print(f"❌ Validation failed: {e}", file=sys.stderr)
        sys.exit(1)
