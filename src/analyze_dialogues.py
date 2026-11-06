import sys
import os
import traceback
import time
import json
from collections import Counter, defaultdict

def main():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/analysis_result.json"

    speaker_counts = Counter()
    word_counts = Counter()

    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {corpus_path}")
        sys.exit(1)

    try:
        with open(corpus_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    speaker = record.get("speaker", "unknown")
                    text = record.get("text", "")
                    speaker_counts[speaker] += 1
                    
                    words = text.split()
                    for word in words:
                        word_counts[word] += 1
                except json.JSONDecodeError:
                    continue

        result = {
            "speaker_counts": dict(speaker_counts),
            "top_words": dict(word_counts.most_common(20))
        }

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as out:
            json.dump(result, out, ensure_ascii=False, indent=2)

        print(f"Analysis complete. Results saved to {output_path}")

    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
