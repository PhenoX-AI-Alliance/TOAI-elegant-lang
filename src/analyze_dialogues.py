import sys
import os
import traceback
import time
import json
import collections

def analyze():
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
                data = json.loads(line)
                speaker = data.get("speaker", "unknown")
                text = data.get("text", "")
                
                speaker_counts[speaker] += 1
                
                words = text.lower().split()
                for word in words:
                    cleaned = "".join(ch for ch in word if ch.isalnum())
                    if cleaned:
                        word_counts[cleaned] += 1

        result = {
            "speaker_counts": dict(speaker_counts),
            "top_words": dict(word_counts.most_common(10)) if hasattr(word_counts, "most_common") else dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10])
        }

        output_dir = "/home/phenox/gemini-sandbox/TOAI_Generated"
        os.makedirs(output_dir, exist_ok=True)
        out_file = os.path.join(output_dir, "dialogue_analysis_result.json")
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Analysis completed successfully. Result saved to {out_file}")

    except Exception as e:
        print(f"An error occurred during analysis: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    analyze()
