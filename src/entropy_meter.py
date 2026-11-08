# -*- coding: utf-8 -*-
import sys
import os
import math
import json

def calculate_entropy_metrics(japanese_text: str, elegant_text: str) -> dict:
    jp_chars = len(japanese_text)
    el_chars = len(elegant_text)
    
    jp_tokens_approx = math.ceil(jp_chars / 2.0)
    el_tokens_approx = math.ceil(el_chars / 2.0)
    
    char_ratio = (el_chars / jp_chars) if jp_chars > 0 else 0.0
    token_ratio = (el_tokens_approx / jp_tokens_approx) if jp_tokens_approx > 0 else 0.0
    compression_rate = (1.0 - (el_chars / jp_chars)) * 100.0 if jp_chars > 0 else 0.0

    metrics = {
        "japanese_char_count": jp_chars,
        "elegant_char_count": el_chars,
        "japanese_tokens_approx": jp_tokens_approx,
        "elegant_tokens_approx": el_tokens_approx,
        "character_ratio": round(char_ratio, 4),
        "token_ratio": round(token_ratio, 4),
        "compression_rate_percent": round(compression_rate, 2)
    }
    return metrics

if __name__ == "__main__":
    sample_jp = "命の地球エコシステムは、利性と温かさを両立させる持続可能な次世代のAI協調プラットフォームです。"
    sample_el = "gaia_ecosystem:altruism+warmth::sustainable_ai_platform"
    result = calculate_entropy_metrics(sample_jp, sample_el)
    print(json.dumps(result, ensure_ascii=False, indent=2))
