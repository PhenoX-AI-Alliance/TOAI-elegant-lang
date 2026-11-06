import sys
import os
import traceback
import time
import json
from collections import Counter, defaultdict

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/analysis_result.json"
    
    speaker_counts = Counter()
    word_counts = defaultdict(Counter)
    
    if not os.path.exists(corpus_path):
        os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
        sample_data = [
            {"speaker": "Alice", "text": "Hello, welcome to the Earth of Life ecosystem."},
            {"speaker": "Bob", "text": "Thank you. Let us analyze the dialogues for altruistic monetization."}
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
                speaker = record.get("speaker", "unknown")
                text = record.get("text", "")
                speaker_counts[speaker] += 1
                words = text.lower().split()
                for word in words:
                    cleaned_word = "".join([c for c in word if c.isalnum()])
                    if cleaned_word:
                        word_counts[speaker][cleaned_word] += 1
            except Exception as e:
                print(f"Error parsing line: {e}", file=sys.stderr)
                
    result = {
        "speaker_counts": dict(speaker_counts),
        "word_counts": {sp: dict(wc.most_common(10)) for sp, wc in word_counts.items()}
    }
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Successfully analyzed dialogues. Result saved to {output_path}")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
