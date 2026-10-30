import sys
import os
import json
from collections import Counter, defaultdict

def analyze():
    base_dir = "/home/phenox/gemini-sandbox"
    corpus_path = os.path.join(base_dir, "corpus", "dialogues.jsonl")
    
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
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
                
                words = [w.strip('.,!?') for w in text.lower().split() if len(w.strip('.,!?')) > 2]
                for w in words:
                    word_counts[speaker][w] += 1
            except Exception as e:
                print(f"Warning: Failed to parse line: {e}")
                
    result = {
        "speaker_counts": dict(speaker_counts),
        "word_frequencies": {sp: dict(cnt.most_common(10)) for sp, cnt in word_counts.items()}
    }
    
    output_path = os.path.join(base_dir, "TOAI_Generated", "dialogue_analysis_result.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        
    print(f"Analysis completed successfully. Result saved to {output_path}")

if __name__ == "__main__":
    analyze()
