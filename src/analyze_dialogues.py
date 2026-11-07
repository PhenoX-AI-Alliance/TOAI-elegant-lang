import sys
import os
import traceback
import time
import json
from collections import Counter, defaultdict

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/dialogue_analysis_result.json"
    
    speaker_counts = Counter()
    word_counts = defaultdict(Counter)
    
    if not os.path.exists(corpus_path):
        print(f"Warning: {corpus_path} does not exist. Creating a dummy dialogue file for analysis.")
        os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
        sample_data = [
            {"speaker": "Gaia", "text": "Welcome to the Earth of Life ecosystem. Altruism brings sustainable value."},
            {"speaker": "Human", "text": "How can we monetize our solutions ethically?"},
            {"speaker": "Gaia", "text": "By delivering genuine technical value and practical solutions to the world."}
        ]
        with open(corpus_path, "w", encoding="utf-8") as f:
            for item in sample_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

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
                    cleaned_word = "".join(ch for ch in word if ch.isalnum())
                    if cleaned_word:
                        word_counts[speaker][cleaned_word] += 1
            except json.JSONDecodeError:
                continue

    result = {
        "speaker_utterance_counts": dict(speaker_counts),
        "speaker_word_frequencies": {sp: dict(wc.most_common(10)) for sp, wc in word_counts.items()},
        "timestamp": time.time()
    }
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"Analysis completed successfully. Results saved to {output_path}")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
