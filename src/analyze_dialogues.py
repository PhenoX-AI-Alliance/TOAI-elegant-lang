import sys
import os
import traceback
import time
import json
from collections import Counter

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {{corpus_path}}", file=sys.stderr)
        sys.exit(1)
        
    speaker_counts = Counter()
    word_counts = Counter()
    
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
                    cleaned = w.strip(".,!?()[]\"'").lower()
                    if cleaned:
                        word_counts[cleaned] += 1
            except Exception as e:
                print(f"Warning: Failed to parse line: {{e}}", file=sys.stderr)
                
    result = {
        "speaker_counts": dict(speaker_counts),
        "top_words": word_counts.most_common(50)
    }
    
    output_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "dialogue_analysis.json")
    
    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(result, out, ensure_ascii=False, indent=2)
        
    print(f"Analysis complete. Results saved to {{output_path}}")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
