# -*- coding: utf-8 -*-
import sys
import os
import time
import json
import zlib

def benchmark_entropy(japanese_text: str, elegant_text: str) -> dict:
    jp_bytes = japanese_text.encode('utf-8')
    el_bytes = elegant_text.encode('utf-8')
    
    jp_len = len(jp_bytes)
    el_len = len(el_bytes)
    
    ratio_length = el_len / jp_len if jp_len > 0 else 0.0
    
    jp_chars = len(japanese_text)
    el_chars = len(elegant_text)
    
    jp_tokens_approx = jp_chars * 1.5
    el_tokens_approx = el_chars * 1.0
    
    ratio_tokens = el_tokens_approx / jp_tokens_approx if jp_tokens_approx > 0 else 0.0
    
    jp_compressed = zlib.compress(jp_bytes)
    el_compressed = zlib.compress(el_bytes)
    
    jp_compression_ratio = len(jp_compressed) / jp_len if jp_len > 0 else 1.0
    el_compression_ratio = len(el_compressed) / el_len if el_len > 0 else 1.0
    
    metrics = {
        "japanese_byte_length": jp_len,
        "elegant_byte_length": el_len,
        "byte_length_ratio": ratio_length,
        "japanese_approx_tokens": jp_tokens_approx,
        "elegant_approx_tokens": el_tokens_approx,
        "token_ratio": ratio_tokens,
        "japanese_compression_ratio": jp_compression_ratio,
        "elegant_compression_ratio": el_compression_ratio,
        "timestamp": time.time()
    }
    return metrics

if __name__ == "__main__":
    sample_jp = "命の地球エコシステムにおいて、利性と温かさを両立させる。"
    sample_el = "Gaia.eco(altruism=warmth, efficiency=balanced)"
    result = benchmark_entropy(sample_jp, sample_el)
    print(json.dumps(result, ensure_ascii=False, indent=2))
