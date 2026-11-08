# -*- coding: utf-8 -*-
import math
import zlib

def calculate_entropy_and_metrics(japanese_text: str, elegant_text: str) -> dict:
    jp_bytes = japanese_text.encode('utf-8')
    el_bytes = elegant_text.encode('utf-8')
    
    jp_len = len(japanese_text)
    el_len = len(elegant_text)
    
    jp_tokens_approx = math.ceil(jp_len / 2.0)
    el_tokens_approx = math.ceil(el_len / 3.0)
    
    jp_compressed = zlib.compress(jp_bytes)
    el_compressed = zlib.compress(el_bytes)
    
    jp_comp_ratio = len(jp_compressed) / len(jp_bytes) if len(jp_bytes) > 0 else 0.0
    el_comp_ratio = len(el_compressed) / len(el_bytes) if len(el_bytes) > 0 else 0.0
    
    char_ratio = el_len / jp_len if jp_len > 0 else 0.0
    token_ratio = el_tokens_approx / jp_tokens_approx if jp_tokens_approx > 0 else 0.0
    
    metrics = {
        "japanese_char_count": jp_len,
        "elegant_char_count": el_len,
        "character_ratio": char_ratio,
        "japanese_approx_tokens": jp_tokens_approx,
        "elegant_approx_tokens": el_tokens_approx,
        "token_ratio": token_ratio,
        "japanese_compression_ratio": jp_comp_ratio,
        "elegant_compression_ratio": el_comp_ratio
    }
    return metrics
