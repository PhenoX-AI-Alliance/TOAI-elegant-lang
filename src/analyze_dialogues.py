import sys
import os
import traceback
import time
import json
import collections

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    output_report = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/analysis_report.json"

    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {corpus_path}")
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
                    cleaned = "".join(c for c in word if c.isalnum())
                    if cleaned:
                        word_counts[cleaned] += 1

        report = {
            "timestamp": time.time(),
            "speaker_counts": dict(speaker_counts),
            "top_words": dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10])
        }

        os.makedirs(os.path.dirname(output_report), exist_ok=True)
        with open(output_report, "w", encoding="utf-8") as out:
            json.dump(report, out, ensure_ascii=False, indent=2)

        print("Analysis completed successfully. Report saved to:", output_report)

    except Exception as e:
        print("An error occurred during analysis:", str(e))
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    analyze()
