import sys
import os
import traceback
import time
import json
import zlib
import math

def calculate_entropy_and_metrics(japanese_text: str, elegant_text: str) -> dict:
    jp_bytes = japanese_text.encode('utf-8')
    el_bytes = elegant_text.encode('utf-8')
    
    jp_len = len(japanese_text)
    el_len = len(elegant_text)
    
    jp_tokens_approx = math.ceil(jp_len / 2.0)
    el_tokens_approx = math.ceil(el_len / 3.0)
    
    jp_compressed = zlib.compress(jp_bytes)
    el_compressed = zlib.compress(el_bytes)
    
    jp_compression_ratio = len(jp_compressed) / len(jp_bytes) if len(jp_bytes) > 0 else 0.0
    el_compression_ratio = len(el_compressed) / len(el_bytes) if len(el_bytes) > 0 else 0.0
    
    char_ratio = el_len / jp_len if jp_len > 0 else 0.0
    token_ratio = el_tokens_approx / jp_tokens_approx if jp_tokens_approx > 0 else 0.0
    
    metrics = {
        "japanese_char_count": jp_len,
        "elegant_char_count": el_len,
        "char_ratio": char_ratio,
        "japanese_tokens_approx": jp_tokens_approx,
        "elegant_tokens_approx": el_tokens_approx,
        "token_ratio": token_ratio,
        "japanese_compression_ratio": jp_compression_ratio,
        "elegant_compression_ratio": el_compression_ratio
    }
    return metrics

def benchmark_entropy(japanese_text: str, elegant_text: str) -> str:
    result = calculate_entropy_and_metrics(japanese_text, elegant_text)
    return json.dumps(result, ensure_ascii=False, indent=4)
