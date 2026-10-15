import sys
import os
import traceback
import time
import json
import collections

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)
    
    if not os.path.exists(corpus_path):
        print(f"Corpus file not found: {corpus_path}")
        sys.exit(1)
        
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                speaker = data.get("speaker", "Unknown")
                speaker_counts[speaker] += 1
                text = data.get("text", "").lower()
                words = text.split()
                for word in words:
                    cleaned = "".join([c for c in word if c.isalnum()])
                    if cleaned:
                        word_counts[cleaned] += 1
            except Exception as e:
                print(f"Parsing error: {e}")
                
    print("=== Speaker Counts ===")
    for spk, cnt in speaker_counts.items():
        print(f"{spk}: {cnt}")
        
    print("\n=== Top Word Frequencies ===")
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    for w, c in sorted_words[:10]:
        print(f"{w}: {c}")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
