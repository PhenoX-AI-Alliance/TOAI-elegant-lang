import sys
import os
import traceback
import time
import json
import collections

def main():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
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
                try:
                    data = json.loads(line)
                    speaker = data.get("speaker", "unknown")
                    speaker_counts[speaker] += 1
                    text = data.get("text", "")
                    for word in text.split():
                        word_counts[word.lower()] += 1
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        print(f"Error reading corpus: {e}")
        traceback.print_exc()
        sys.exit(1)

    result = {
        "speaker_counts": dict(speaker_counts),
        "top_words": dict(word_counts.most_common(50) if hasattr(word_counts, "most_common") else sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:50])
    }

    output_result_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/dialogue_analysis_result.json"
    try:
        with open(output_result_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Successfully analyzed dialogues. Results saved to {output_result_path}")
    except Exception as e:
        print(f"Error saving analysis results: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Unhandled exception: {e}")
        traceback.print_exc()
        sys.exit(1)
