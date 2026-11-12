import sys
import os
import traceback
import time
import json
from collections import Counter, defaultdict

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {corpus_path}")
        sys.exit(1)
        
    speaker_counts = Counter()
    word_counts = defaultdict(Counter)
    
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                speaker = data.get("speaker", "Unknown")
                text = data.get("text", "")
                
                speaker_counts[speaker] += 1
                
                words = text.lower().split()
                for word in words:
                    cleaned = "".join(ch for ch in word if ch.isalnum())
                    if cleaned:
                        word_counts[speaker][cleaned] += 1
            except Exception as e:
                print(f"Warning: Failed to parse line: {e}")
                
    result = {
        "speaker_utterance_counts": dict(speaker_counts),
        "speaker_word_frequencies": {sp: dict(cnt) for sp, cnt in word_counts.items()}
    }
    
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/analysis_result.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        
    print(f"Analysis successfully completed. Results saved to {output_path}")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
