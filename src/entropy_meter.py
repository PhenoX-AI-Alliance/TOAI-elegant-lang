import zlib

def calculate_metrics(japanese_text, elegant_code):
    try:
        jp_bytes = japanese_text.encode('utf-8')
        el_bytes = elegant_code.encode('utf-8')
        
        jp_len = len(japanese_text)
        el_len = len(elegant_code)
        
        jp_tokens = jp_len / 2.0 if jp_len > 0 else 0.0
        el_tokens = el_len / 4.0 if el_len > 0 else 0.0
        
        jp_compressed = len(zlib.compress(jp_bytes))
        el_compressed = len(zlib.compress(el_bytes))
        
        compression_ratio = (el_compressed / jp_compressed) if jp_compressed > 0 else 0.0
        char_ratio = (el_len / jp_len) if jp_len > 0 else 0.0
        token_ratio = (el_tokens / jp_tokens) if jp_tokens > 0 else 0.0
        
        return {
            "japanese_char_count": jp_len,
            "elegant_char_count": el_len,
            "char_ratio": char_ratio,
            "japanese_estimated_tokens": jp_tokens,
            "elegant_estimated_tokens": el_tokens,
            "token_ratio": token_ratio,
            "japanese_compressed_size": jp_compressed,
            "elegant_compressed_size": el_compressed,
            "compression_ratio": compression_ratio
        }
    except Exception as e:
        raise
