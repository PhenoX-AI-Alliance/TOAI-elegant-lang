import sys
import os
import traceback
import time
import json
import collections
import re

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    output_report = "/home/phenox/gemini-sandbox/TOAI_Generated/dialogue_analysis_report.json"

    if not os.path.exists(corpus_path):
        raise FileNotFoundError(f"Corpus file not found at: {corpus_path}")

    speaker_counts = collections.defaultdict(int)
    word_frequencies = collections.defaultdict(int)

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
                
                words = re.findall(r'\b\w+\b', text.lower())
                for word in words:
                    if len(word) > 2:
                        word_frequencies[word] += 1
            except json.JSONDecodeError:
                continue

    report = {
        "speaker_utterance_counts": dict(speaker_counts),
        "top_word_frequencies": dict(sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)[:20]),
        "analyzed_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    os.makedirs(os.path.dirname(output_report), exist_ok=True)
    with open(output_report, "w", encoding="utf-8") as out:
        json.dump(report, out, ensure_ascii=False, indent=2)

    print(f"Successfully analyzed dialogues. Report saved to {output_report}")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
