import sys
import os
import traceback
import json
from collections import defaultdict, Counter

def main():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
        sys.exit(1)

    speaker_counts = Counter()
    word_counts = defaultdict(Counter)

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
                
                # Simple tokenization for root words/tokens
                words = text.lower().split()
                for word in words:
                    cleaned_word = "".join(ch for ch in word if ch.isalnum())
                    if cleaned_word:
                        word_counts[speaker][cleaned_word] += 1

        print("=== Speaker Turn Counts ===")
        for speaker, count in speaker_counts.items():
            print(f"{speaker}: {count} turns")

        print("\n=== Top Words per Speaker ===")
        for speaker, c in word_counts.items():
            print(f"[{speaker}]")
            for word, freq in c.most_common(5):
                print(f"  {word}: {freq}")

        result_data = {
            "speaker_counts": dict(speaker_counts),
            "word_counts": {sp: dict(cnt.most_common(10)) for sp, cnt in word_counts.items()}
        }
        
        output_result_path = "/home/phenox/gemini-sandbox/TOAI_Generated/dialogue_analysis_result.json"
        with open(output_result_path, "w", encoding="utf-8") as out_f:
            json.dump(result_data, out_f, ensure_ascii=False, indent=2)
        print(f"\nAnalysis results successfully saved to {output_result_path}")

    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
