# -*- coding: utf-8 -*-
import sys
import os
import traceback
import time
import json
import re

def parse_telepath_expr(expression):
    pattern = re.compile(r'^\s*(?P<source>.+?)\s*-\[\s*p\s*:\s*(?P<prob>[\d\.]+)\s*(?:,\s*r\s*:\s*(?P<reward>[\d\.-]+))?\s*\]->\s*(?P<target>.+?)\s*$')
    match = pattern.match(expression)
    if not match:
        raise ValueError(f"Invalid telepath expression syntax: {expression}")
    
    data = match.groupdict()
    source = data['source'].strip()
    target = data['target'].strip()
    prob = float(data['prob'])
    reward = float(data['reward']) if data['reward'] is not None else 0.0
    
    return {
        "source": source,
        "target": target,
        "probability": prob,
        "reward": reward
    }
