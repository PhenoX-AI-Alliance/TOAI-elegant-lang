# -*- coding: utf-8 -*-
import re

def parse_telepath_expr(expression_str):
    pattern = re.compile(r'^\s*([A-Za-z0-9_]+)\s*-\[([^\]]+)\]->\s*([A-Za-z0-9_]+)\s*$')
    match = pattern.match(expression_str)
    if not match:
        raise ValueError(f"Invalid expression format: {expression_str}")
    
    source = match.group(1)
    meta_str = match.group(2)
    target = match.group(3)
    
    meta_dict = {}
    parts = meta_str.split(',')
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if ':' in part:
            key, val = part.split(':', 1)
            key = key.strip()
            val = val.strip()
            try:
                if '.' in val:
                    val = float(val)
                else:
                    val = int(val)
            except ValueError:
                pass
            meta_dict[key] = val
        else:
            meta_dict['label'] = part

    return {
        "source": source,
        "target": target,
        "metadata": meta_dict
    }
