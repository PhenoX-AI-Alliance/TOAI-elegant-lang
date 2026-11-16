import sys
import os
import json
from collections import Counter

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
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
            data = json.loads(line)
            speaker = data.get("speaker", "unknown")
            text = data.get("text", "")
            
            speaker_counts[speaker] += 1
            
            words = text.lower().split()
            for w in words:
                cleaned = "".join(ch for ch in w if ch.isalnum())
                if cleaned:
                    word_counts[cleaned] += 1
                    
    result = {
        "speaker_counts": dict(speaker_counts),
        "top_words": word_counts.most_common(10)
    }
    
    output_dir = "/home/phenox/gemini-sandbox/TOAI_Generated"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "dialogue_analysis_result.json")
    
    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(result, out, ensure_ascii=False, indent=2)
        
    print(f"Analysis successfully completed and saved to {output_path}")

if __name__ == "__main__":
    analyze()
