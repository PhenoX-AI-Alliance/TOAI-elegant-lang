#!/usr/bin/env python3
"""
Compatibility wrapper for `benchmarks/eval_comprehension.py` (v5.4.3).
Allows invoking `python examples/eval_comprehension.py ...` or `python benchmarks/eval_comprehension.py ...` interchangeably.
"""
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

if __name__ == "__main__":
    target = ROOT / "benchmarks" / "eval_comprehension.py"
    runpy.run_path(str(target), run_name="__main__")
