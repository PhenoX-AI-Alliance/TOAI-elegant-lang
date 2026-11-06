import sys
import os
import traceback
import time
import json
import collections

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: {corpus_path} not found.")
        sys.exit(1)
        
    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)
    
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                speaker = data.get("speaker", "unknown")
                text = data.get("text", "")
                
                speaker_counts[speaker] += 1
                
                words = text.lower().split()
                for w in words:
                    cleaned = "".join(c for c in w if c.isalnum())
                    if cleaned:
                        word_counts[cleaned] += 1
            except Exception as e:
                print(f"Warning: Failed to parse line: {e}")
                
    result = {
        "speaker_counts": dict(speaker_counts),
        "top_words": dict(word_counts.most_common(10))
    }
    
    output_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "analysis_result.json")
    
    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(result, out, indent=2, ensure_ascii=False)
        
    print(f"Successfully analyzed dialogues. Result saved to {output_path}")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
