import sys
import os
import traceback
import time
import json
from collections import Counter

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {corpus_path}")
        sys.exit(1)
        
    speaker_counts = Counter()
    word_counts = Counter()
    
    try:
        with open(corpus_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    speaker = data.get("speaker", "unknown")
                    text = data.get("text", "")
                    speaker_counts[speaker] += 1
                    words = text.lower().split()
                    for w in words:
                        cleaned = "".join(ch for ch in w if ch.isalnum())
                        if cleaned:
                            word_counts[cleaned] += 1
                except json.JSONDecodeError as jde:
                    print(f"Warning: JSON decode error at line {line_num}: {jde}")
                    
        print("=== Speaker Frequencies ===")
        for spk, cnt in speaker_counts.items():
            print(f"{spk}: {cnt}")
            
        print("\n=== Top Root/Word Frequencies ===")
        for w, cnt in word_counts.most_common(10):
            print(f"{w}: {cnt}")
            
        result_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/results"
        os.makedirs(result_dir, exist_ok=True)
        result_path = os.path.join(result_dir, "dialogue_analysis.json")
        
        output_data = {
            "speakers": dict(speaker_counts),
            "top_words": dict(word_counts.most_common(20)),
            "timestamp": time.time()
        }
        
        with open(result_path, "w", encoding="utf-8") as rf:
            json.dump(output_data, rf, ensure_ascii=False, indent=2)
            
        print(f"Analysis successfully completed and saved to {result_path}")
        
    except Exception as e:
        print(f"An unexpected error occurred during analysis: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    analyze()
