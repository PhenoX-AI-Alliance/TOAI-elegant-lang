import sys
import os
import traceback
import time
import json
import collections
import re

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    output_report_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/dialogue_analysis_report.json"

    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)

    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
        sys.exit(1)

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

                words = re.findall(r"\w+", text.lower())
                for word in words:
                    if len(word) > 2:
                        word_counts[word] += 1
            except json.JSONDecodeError:
                continue

    report = {
        "speaker_counts": dict(speaker_counts),
        "top_words": dict(word_counts.most_common(50)),
        "analyzed_at": time.time()
    }

    os.makedirs(os.path.dirname(output_report_path), exist_ok=True)
    with open(output_report_path, "w", encoding="utf-8") as out:
        json.dump(report, out, ensure_ascii=False, indent=2)

    print(f"Analysis complete. Report saved to {output_report_path}")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
