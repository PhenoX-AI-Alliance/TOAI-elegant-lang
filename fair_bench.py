#!/usr/bin/env python3
"""Root-level entry point for `benchmarks/fair_bench.py`."""
import sys
from pathlib import Path

BENCH_DIR = Path(__file__).resolve().parent / "benchmarks"
if str(BENCH_DIR) not in sys.path:
    sys.path.insert(0, str(BENCH_DIR))

from fair_bench import run_fair_benchmark

if __name__ == "__main__":
    run_fair_benchmark()
