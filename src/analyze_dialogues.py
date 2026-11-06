import sys
import os
import traceback
import time
import json
from collections import defaultdict, Counter

def analyze_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    output_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "dialogue_analysis.json")

    speaker_counts = Counter()
    word_counts = defaultdict(Counter)

    if not os.path.exists(corpus_path):
        print(f"Corpus file not found: {corpus_path}")
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
                        clean_word = word.strip(".,!?()[]\"'").lower()
                        if clean_word:
                            word_counts[speaker][clean_word] += 1
                except json.JSONDecodeError:
                    continue

        results = {
            "speaker_utterance_counts": dict(speaker_counts),
            "speaker_word_frequencies": {sp: dict(cnt.most_common(50)) for sp, cnt in word_counts.items()}
        }

        with open(output_path, "w", encoding="utf-8") as out_f:
            json.dump(results, out_f, ensure_ascii=False, indent=2)

        print(f"Analysis successfully completed. Results saved to {output_path}")

    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    analyze_dialogues()
