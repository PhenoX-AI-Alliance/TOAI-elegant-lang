import sys
import os
import traceback
import time
import json
import collections

def run_analysis():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print("Error: corpus dialogues.jsonl not found.")
        sys.exit(1)
        
    speaker_counts = collections.defaultdict(int)
    word_frequencies = collections.defaultdict(int)
    
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
                for word in text.lower().split():
                    cleaned = "".join([c for c in word if c.isalnum()])
                    if cleaned:
                        word_frequencies[cleaned] += 1
                        
        print("=== Speaker Counts ===")
        for s, count in speaker_counts.items():
            print(s + ": " + str(count))
            
        print("=== Top Word Frequencies ===")
        sorted_words = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)
        for w, count in sorted_words[:10]:
            print(w + ": " + str(count))
            
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_analysis()
