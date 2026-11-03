# -*- coding: utf-8 -*-
import re

def parse_telepath_expr(expression):
    pattern = re.compile(r'^\s*([A-Za-z0-9_]+)\s*-\s*\[\s*p\s*:\s*([0-9\.]+)(?:\s*,\s*r\s*:\s*([0-9\.\-]+))?\s*\]\s*->\s*([A-Za-z0-9_]+)\s*$')
    match = pattern.match(expression)
    if not match:
        raise ValueError(f"Invalid telepath expression format: {expression}")
    
    source = match.group(1)
    probability = float(match.group(2))
    reward_str = match.group(3)
    reward = float(reward_str) if reward_str is not None else 0.0
    target = match.group(4)
    
    return {
        "source": source,
        "probability": probability,
        "reward": reward,
        "target": target
    }
