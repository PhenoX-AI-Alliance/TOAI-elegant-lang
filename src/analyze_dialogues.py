import sys
import os
import traceback
import time
import json
from collections import Counter

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {corpus_path}")
        sys.exit(1)
        
    speaker_counts = Counter()
    word_counts = Counter()
    
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
                for w in words:
                    cleaned = ''.join(c for c in w if c.isalnum())
                    if cleaned:
                        word_counts[cleaned] += 1
            except Exception as e:
                print(f"Warning: Failed to parse line: {e}")
                
    result = {
        "speaker_counts": dict(speaker_counts),
        "top_words": word_counts.most_common(20)
    }
    
    output_json_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/analysis_result.json"
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully analyzed dialogues. Results saved to {output_json_path}")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
