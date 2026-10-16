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
        print("Corpus file not found.")
        sys.exit(1)

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            speaker = record.get("speaker", "unknown")
            text = record.get("text", "")
            speaker_counts[speaker] += 1
            words = text.lower().split()
            for word in words:
                cleaned = "".join([c for c in word if c.isalnum()])
                if cleaned:
                    word_counts[cleaned] += 1

    print("Speaker Counts:", dict(speaker_counts))
    print("Word Frequencies:", dict(word_counts))

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
