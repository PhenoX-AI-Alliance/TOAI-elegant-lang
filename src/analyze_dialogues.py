import sys
import os
import json
from collections import Counter

def main():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Corpus file not found: {corpus_path}", file=sys.stderr)
        sys.exit(1)
        
    speaker_counts = Counter()
    word_counts = Counter()
    
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if not line_str:
                continue
            try:
                record = json.loads(line_str)
                speaker = record.get("speaker", "unknown")
                text = record.get("text", "")
                speaker_counts[speaker] += 1
                
                words = text.lower().split()
                for w in words:
                    cleaned = "".join([c for c in w if c.isalnum()])
                    if cleaned:
                        word_counts[cleaned] += 1
            except Exception as e:
                print(f"Failed to parse record: {e}", file=sys.stderr)
                
    print("=== Speaker Counts ===")
    for spk, cnt in speaker_counts.items():
        print(f"{spk}: {cnt}")
        
    print("\n=== Top Roots/Words ===")
    for word, cnt in word_counts.most_common(10):
        print(f"{word}: {cnt}")

if __name__ == "__main__":
    main()
