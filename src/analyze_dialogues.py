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
        print(f"Error: Corpus not found at {corpus_path}")
        sys.exit(1)

    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)

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
                
                words = re.findall(r'[a-zA-Z]+', text.lower())
                for w in words:
                    if len(w) > 2:
                        word_counts[w] += 1
            except Exception as e:
                print(f"Warning: Failed to parse line: {e}")

    output_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "analysis_result.json")

    result = {
        "speaker_counts": dict(speaker_counts),
        "top_words": dict(word_counts.most_common(20)),
        "timestamp": time.time()
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Analysis successfully completed. Result saved to {output_path}")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
