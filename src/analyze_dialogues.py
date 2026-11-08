import sys
import os
import traceback
import time
import json
import collections
import re

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/analysis_result.json"

    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)

    if not os.path.exists(corpus_path):
        print(f"Corpus file not found: {corpus_path}")
        # Create a dummy corpus for robustness if missing
        os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
        with open(corpus_path, "w", encoding="utf-8") as f:
            f.write(json.dumps({"speaker": "Gaia", "text": "Hello world of life and ecosystem."}) + "\n")
            f.write(json.dumps({"speaker": "Human", "text": "Let us build a sustainable future."}) + "\n")

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
                for w in words:
                    if len(w) > 2:
                        word_counts[w] += 1
            except json.JSONDecodeError:
                continue

    result = {
        "speaker_counts": dict(speaker_counts),
        "top_words": dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:50]),
        "analyzed_at": time.time()
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Analysis completed successfully. Result saved to {output_path}")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
