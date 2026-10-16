import sys
import os
import traceback
import time
import json
import collections

def analyze():
    corpus_file = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_file):
        print("Corpus file not found.", file=sys.stderr)
        sys.exit(1)
        
    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)
    
    with open(corpus_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            speaker = record.get("speaker", "Unknown")
            text = record.get("text", "")
            speaker_counts[speaker] += 1
            for word in text.lower().split():
                cleaned = "".join([c for c in word if c.isalnum()])
                if cleaned:
                    word_counts[cleaned] += 1
                    
    print("Speaker Counts:", dict(speaker_counts))
    print("Top Words:", sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10])

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
