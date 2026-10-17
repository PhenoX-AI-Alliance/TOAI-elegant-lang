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

    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
        sys.exit(1)

    speaker_counts = collections.defaultdict(int)
    word_freq = collections.defaultdict(int)

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                speaker = data.get("speaker", "unknown")
                text = data.get("text", "")
                speaker_counts[speaker] += 1

                words = re.findall(r'[a-zA-Z]+', text.lower())
                for word in words:
                    if len(word) > 2:
                        word_freq[word] += 1
            except Exception as e:
                print(f"Warning: Failed to parse line: {e}")

    result = {
        "speaker_counts": dict(speaker_counts),
        "top_words": dict(sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]),
        "timestamp": time.time()
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Analysis completed successfully. Results saved to {output_path}")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
