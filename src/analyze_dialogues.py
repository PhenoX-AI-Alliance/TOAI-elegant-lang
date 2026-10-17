# -*- coding: utf-8 -*-
import sys
import os
import traceback
import time
import json
from collections import defaultdict, Counter

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print("Corpus file not found: " + corpus_path)
        sys.exit(1)

    speaker_counts = Counter()
    word_counts = defaultdict(Counter)

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                speaker = data.get("speaker", "Unknown")
                text = data.get("text", "")
                speaker_counts[speaker] += 1
                
                words = text.lower().split()
                for w in words:
                    cleaned = "".join(ch for ch in w if ch.isalnum())
                    if cleaned:
                        word_counts[speaker][cleaned] += 1
            except Exception as e:
                print("Warning: Failed to parse line: " + str(e))

    result = {
        "speaker_counts": dict(speaker_counts),
        "word_frequencies": {sp: dict(cnt.most_common(10)) for sp, cnt in word_counts.items()}
    }

    output_result_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/analysis_result.json"
    with open(output_result_path, "w", encoding="utf-8") as out:
        json.dump(result, out, ensure_ascii=False, indent=2)

    print("Successfully analyzed dialogues and saved to " + output_result_path)

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
