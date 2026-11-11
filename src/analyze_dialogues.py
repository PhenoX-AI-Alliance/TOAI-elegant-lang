import sys
import os
import traceback
import time
import json
import collections
import re

def analyze():
    base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
    corpus_path = os.path.join(base_dir, "corpus", "dialogues.jsonl")
    output_path = os.path.join(base_dir, "TOAI_Generated", "dialogue_analysis_result.json")

    if not os.path.exists(corpus_path):
        raise FileNotFoundError(f"Corpus not found at {corpus_path}")

    speaker_counts = collections.defaultdict(int)
    word_freq = collections.defaultdict(int)

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            speaker = data.get("speaker", "unknown")
            text = data.get("text", "")

            speaker_counts[speaker] += 1

            words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
            for w in words:
                word_freq[w] += 1

    result = {
        "speaker_counts": dict(speaker_counts),
        "top_words": sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(result, out, ensure_ascii=False, indent=2)

    print(f"Analysis successfully completed. Result saved to {output_path}")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
