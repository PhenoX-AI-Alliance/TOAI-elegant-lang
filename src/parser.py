import re

def parse_telepath_expr(expression):
    pattern = r"^\\s*(.+?)\\s*-\\s*\[\\s*p\\s*:\\s*([0-9\\.]+)(?:\\s*,\\s*r\\s*:\\s*([0-9\\.\\-]+))?\\s*\]->\\s*(.+?)\\s*$"
    match = re.match(pattern, expression)
    if not match:
        raise ValueError(f"Invalid telepath expression format: {expression}")
    
    source = match.group(1).strip()
    probability = float(match.group(2))
    reward_str = match.group(3)
    reward = float(reward_str) if reward_str is not None else 0.0
    target = match.group(4).strip()
    
    return {
        "source": source,
        "probability": probability,
        "reward": reward,
        "target": target
    }
