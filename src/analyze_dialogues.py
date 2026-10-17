import sys
import os
import traceback
import time
import json
import collections

def analyze():
    corpus_file = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_file):
        print("Corpus file not found.")
        sys.exit(1)
        
    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)
    
    with open(corpus_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            speaker = record.get("speaker", "unknown")
            text = record.get("text", "")
            speaker_counts[speaker] += 1
            for word in text.lower().split():
                cleaned = "".join(ch for ch in word if ch.isalnum())
                if cleaned:
                    word_counts[cleaned] += 1
                    
    result = {
        "speaker_counts": dict(speaker_counts),
        "word_counts": dict(word_counts)
    }
    out_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/dialogue_analysis.json"
    with open(out_path, "w", encoding="utf-8") as out:
        json.dump(result, out, ensure_ascii=False, indent=2)
    print("Analysis completed successfully.")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
