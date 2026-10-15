import sys
import os
import traceback
import time
import json
import collections

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Corpus not found at {corpus_path}")
        sys.exit(1)
        
    speaker_counts = collections.Counter()
    word_counts = collections.Counter()
    
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            speaker = record.get("speaker", "Unknown")
            text = record.get("text", "")
            speaker_counts[speaker] += 1
            words = text.lower().replace(",", "").replace(".", "").split()
            for w in words:
                word_counts[w] += 1
                
    print("Speaker Counts:", dict(speaker_counts))
    print("Top Words:", word_counts.most_common(10))

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
