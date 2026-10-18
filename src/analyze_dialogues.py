import sys
import os
import traceback
import time
import json
import collections
import re

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Corpus not found at {corpus_path}")
        sys.exit(1)
        
    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)
    
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            speaker = record.get("speaker", "Unknown")
            text = record.get("text", "")
            speaker_counts[speaker] += 1
            words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
            for w in words:
                word_counts[w] += 1
                
    result = {
        "speaker_counts": dict(speaker_counts),
        "word_counts": dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True))
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
