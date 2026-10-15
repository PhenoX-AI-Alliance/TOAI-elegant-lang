import sys
import os
import traceback
import time
import json
import collections

def analyze_corpus():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    output_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/output"
    os.makedirs(output_dir, exist_ok=True)
    output_result_path = os.path.join(output_dir, "analysis_result.json")

    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
        sys.exit(1)

    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)

    try:
        with open(corpus_path, "r", encoding="utf-8") as f:
            for line in f:
                line_str = line.strip()
                if not line_str:
                    continue
                try:
                    data = json.loads(line_str)
                    speaker = data.get("speaker", "unknown")
                    speaker_counts[speaker] += 1
                    
                    text = data.get("text", "")
                    tokens = text.split()
                    for token in tokens:
                        root = token.lower().strip(".,!?:;\"'")
                        if root:
                            word_counts[root] += 1
                except json.JSONDecodeError:
                    continue

        result = {
            "speaker_counts": dict(speaker_counts),
            "top_words": dict(word_counts.most_common(50))
        }

        with open(output_result_path, "w", encoding="utf-8") as out_f:
            json.dump(result, out_f, ensure_ascii=False, indent=2)

        print(f"Analysis completed successfully. Results saved to {output_result_path}")

    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    analyze_corpus()
