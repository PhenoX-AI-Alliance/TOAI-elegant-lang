import sys
import os
import traceback
import time
import json
from collections import Counter, defaultdict

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    output_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "dialogue_analysis.json")

    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {corpus_path}")
        sys.exit(1)

    speaker_counts = Counter()
    word_frequencies = defaultdict(Counter)

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
                
                # Simple tokenization by whitespace and lowercasing for root/word frequency
                tokens = text.lower().split()
                for token in tokens:
                    # Clean punctuation
                    cleaned_token = "".join(c for c in token if c.isalnum())
                    if cleaned_token:
                        word_frequencies[speaker][cleaned_token] += 1
            except json.JSONDecodeError:
                continue

    result = {
        "speaker_utterance_counts": dict(speaker_counts),
        "speaker_word_frequencies": {sp: dict(cnt.most_common(50)) for sp, cnt in word_frequencies.items()}
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Successfully analyzed dialogues. Results saved to {output_path}")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
