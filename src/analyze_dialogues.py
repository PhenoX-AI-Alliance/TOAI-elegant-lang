import sys
import os
import traceback
import time
import json
from collections import defaultdict, Counter

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/analysis_result.json"
    
    speaker_counts = Counter()
    word_counts = Counter()
    
    if not os.path.exists(corpus_path):
        print(f"Corpus file not found: {corpus_path}")
        sys.exit(1)
        
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
                
                words = text.split()
                for w in words:
                    cleaned = w.strip('.,!?()[]{}"\'').lower()
                    if cleaned:
                        word_counts[cleaned] += 1
            except Exception as e:
                print(f"Error parsing line: {e}")
                
    result = {
        "speaker_counts": dict(speaker_counts),
        "top_words": dict(word_counts.most_common(50))
    }
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(result, out, ensure_ascii=False, indent=2)
        
    print("Analysis successfully completed.")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
