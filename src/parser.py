# -*- coding: utf-8 -*-
import re

def parse_telepath_expr(expression_str):
    pattern = re.compile(r'^\s*([A-Za-z0-9_]+)\s*-\[([^\]]+)\]->\s*([A-Za-z0-9_]+)\s*$')
    match = pattern.match(expression_str)
    if not match:
        raise ValueError(f"Invalid telepath expression format: {expression_str}")
    
    source = match.group(1)
    meta_str = match.group(2)
    target = match.group(3)
    
    prob = None
    reward = None
    
    parts = meta_str.split(',')
    for part in parts:
        part = part.strip()
        if ':' in part:
            key, val = part.split(':', 1)
            key = key.strip()
            val = val.strip()
            if key == 'p':
                prob = float(val)
            elif key == 'r':
                reward = float(val)
                
    result = {
        "source": source,
        "target": target,
        "probability": prob,
        "reward": reward,
        "raw_meta": meta_str
    }
    return result
