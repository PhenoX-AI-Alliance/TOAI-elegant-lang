# -*- coding: utf-8 -*-
import sys
import os
import math
import zlib

def calculate_entropy_and_metrics(jp_text: str, elegant_text: str) -> dict:
    jp_bytes = jp_text.encode('utf-8')
    elegant_bytes = elegant_text.encode('utf-8')
    
    jp_len = len(jp_text)
    elegant_len = len(elegant_text)
    
    char_ratio = (elegant_len / jp_len) if jp_len > 0 else 0.0
    
    jp_tokens_approx = math.ceil(jp_len / 2.0)
    elegant_tokens_approx = math.ceil(elegant_len / 4.0)
    token_ratio = (elegant_tokens_approx / jp_tokens_approx) if jp_tokens_approx > 0 else 0.0
    
    jp_compressed = zlib.compress(jp_bytes)
    elegant_compressed = zlib.compress(elegant_bytes)
    
    jp_compression_rate = len(jp_compressed) / len(jp_bytes) if len(jp_bytes) > 0 else 0.0
    elegant_compression_rate = len(elegant_compressed) / len(elegant_bytes) if len(elegant_bytes) > 0 else 0.0
    
    metrics = {
        "jp_char_count": jp_len,
        "elegant_char_count": elegant_len,
        "char_ratio": char_ratio,
        "jp_tokens_approx": jp_tokens_approx,
        "elegant_tokens_approx": elegant_tokens_approx,
        "token_ratio": token_ratio,
        "jp_compression_rate": jp_compression_rate,
        "elegant_compression_rate": elegant_compression_rate
    }
    return metrics

if __name__ == "__main__":
    sample_jp = "命の地球エコシステムにおいて、利他と温かさを大切にしながら効率的なコード生成を行います。"
    sample_el = "GaiaEco.altruistic().warmth().generate_code(efficiency=HIGH);"
    result = calculate_entropy_and_metrics(sample_jp, sample_el)
    print("Entropy Benchmark Result:", result)
