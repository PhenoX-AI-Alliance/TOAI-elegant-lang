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
    word_counts = collections.defaultdict(int)

    try:
        with open(corpus_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                speaker = data.get("speaker", "Unknown")
                text = data.get("text", "")

                speaker_counts[speaker] += 1

                words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
                for w in words:
                    word_counts[w] += 1

        result = {
            "speaker_counts": dict(speaker_counts),
            "top_words": dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10])
        }

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as out:
            json.dump(result, out, ensure_ascii=False, indent=2)

        print("Analysis completed successfully.")
        print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        print(f"An error occurred during analysis: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    analyze()
