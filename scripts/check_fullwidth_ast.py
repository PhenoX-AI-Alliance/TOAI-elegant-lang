#!/usr/bin/env python3
"""
AST & Token-based Full-Width Prohibition Verifier.
Checks Python files, specs, and markdown for strictly prohibited full-width alphanumeric/spaces.
"""
import sys
import os
from pathlib import Path

# gemini-sandboxの共通サニタイザーモジュールをロード
SANDBOX_DIR = Path(__file__).resolve().parents[2]
if str(SANDBOX_DIR) not in sys.path:
    sys.path.insert(0, str(SANDBOX_DIR))

try:
    from toai_sanitizer import detect_fullwidth_alphanumeric_and_spaces
except ImportError:
    print("[AST Verifier] Warning: toai_sanitizer not found in path, skipping.")
    sys.exit(0)

def main():
    target_files = sys.argv[1:]
    if not target_files:
        sys.exit(0)

    has_violation = False
    for fpath_str in target_files:
        fpath = Path(fpath_str)
        if not fpath.exists() or not fpath.is_file():
            continue
        # ソースコードおよびマークダウンを検査
        if fpath.suffix not in ('.py', '.md', '.json', '.jsonl'):
            continue
        try:
            content = fpath.read_text(encoding='utf-8')
        except Exception:
            continue

        is_py = (fpath.suffix == '.py')
        violations = detect_fullwidth_alphanumeric_and_spaces(content, is_python=is_py, global_only=is_py)
        if violations:
            has_violation = True
            print(f"❌ [Pre-commit Rule Violation] Full-width characters detected in {fpath}:")
            for v in violations[:5]:
                print(f"   Line {v.get('line')}, Col {v.get('col')}: character '{v.get('char')}' ({v.get('type')})")
            if len(violations) > 5:
                print(f"   ... and {len(violations) - 5} more occurrences.")

    if has_violation:
        print("\nRule 'Global: Full-width characters (alphanumeric/spaces) are strictly prohibited' was violated.")
        print("Please sanitize with toai_sanitizer before committing.")
        sys.exit(1)

    print("✅ [AST Verifier] Full-width prohibition check passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
