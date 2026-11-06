import sys
import os
import traceback
import time
import json
from collections import Counter, defaultdict

def analyze():
    corpus_file = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_file):
        print(f"Corpus file not found: {corpus_file}", file=sys.stderr)
        sys.exit(1)
        
    speaker_counts = Counter()
    word_counts = defaultdict(Counter)
    
    with open(corpus_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            speaker = record.get("speaker", "Unknown")
            text = record.get("text", "")
            speaker_counts[speaker] += 1
            words = text.lower().split()
            for w in words:
                cleaned_w = "".join(ch for ch in w if ch.isalnum())
                if cleaned_w:
                    word_counts[speaker][cleaned_w] += 1
                    
    print("--- Speaker Frequencies ---")
    for sp, count in speaker_counts.items():
        print(f"{sp}: {count}")
        
    print("\n--- Word Frequencies ---")
    for sp, cnt in word_counts.items():
        print(f"Speaker: {sp}")
        for word, freq in cnt.most_common(5):
            print(f"  {word}: {freq}")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
