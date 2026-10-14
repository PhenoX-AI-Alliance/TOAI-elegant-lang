import sys
import os
import traceback
import time
import json
import collections

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {corpus_path}")
        sys.exit(1)

    speaker_counts = collections.Counter()
    word_counts = collections.Counter()

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                speaker = record.get("speaker", "Unknown")
                text = record.get("text", "")
                speaker_counts[speaker] += 1
                
                words = text.lower().split()
                for word in words:
                    cleaned = "".join(c for c in word if c.isalnum())
                    if cleaned:
                        word_counts[cleaned] += 1
            except Exception as e:
                print(f"Warning: Failed to parse line: {e}")

    result = {
        "speaker_counts": dict(speaker_counts),
        "top_words": word_counts.most_common(10)
    }

    output_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/results"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "dialogue_analysis.json")

    with open(output_file, "w", encoding="utf-8") as out:
        json.dump(result, out, ensure_ascii=False, indent=2)

    print(f"Analysis successfully completed. Results saved to {output_file}")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
