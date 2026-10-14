# -*- coding: utf-8 -*-
import sys
import os
import traceback
import time
import json
import collections
import re

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/analysis_result.json"

    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)

    if not os.path.exists(corpus_path):
        print(f"Corpus not found at {{corpus_path}}", file=sys.stderr)
        sys.exit(1)

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

    top_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:50]

    result = {
        "timestamp": time.time(),
        "speaker_counts": dict(speaker_counts),
        "top_words": dict(top_words)
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("Successfully analyzed dialogues and saved result.")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
