import sys
import os
import traceback
import time
import json
from collections import Counter, defaultdict

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/analysis_result.json"
    
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {{corpus_path}}", file=sys.stderr)
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
                    cleaned = w.strip(".,!?\"'()[]{}:;").lower()
                    if cleaned:
                        word_counts[cleaned] += 1
            except json.JSONDecodeError:
                continue
                
    result = {
        "speaker_counts": dict(speaker_counts.most_common()),
        "top_words": dict(word_counts.most_common(50))
    }
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as out_f:
        json.dump(result, out_f, ensure_ascii=False, indent=2)
        
    print(f"Successfully analyzed dialogues. Results saved to {{output_path}}")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
